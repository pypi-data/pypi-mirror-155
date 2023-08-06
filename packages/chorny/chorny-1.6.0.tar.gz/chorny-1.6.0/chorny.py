import dis
from importlib.machinery import ExtensionFileLoader, SourceFileLoader
from pathlib import Path


def _patch_function(func, new_code, new_names):
    func.__code__ = func.__code__.replace(co_code=new_code, co_names=new_names)


def _no_mypyc_for_black(cls, fullname, path):
    if fullname.startswith("black.") or fullname == "black":
        path = Path(path)
        name = path.name
        path = path.with_name(f"{name[:name.find('.')]}.py")
        return SourceFileLoader(fullname, str(path))
    return object.__new__(cls)


def patch_black():
    ExtensionFileLoader.__new__ = _no_mypyc_for_black  # there is no way back
    import black
    from black import (
        _format_str_once,
        format_file_contents,
        Line,
        patched_main,
        syms,
        token,
        transform_line,
    )
    from black.nodes import is_one_sequence_between
    from blib2to3.pytree import Leaf

    def transform_line_patch(line, mode, features=()):
        for transformed_line in transform_line(line, mode, features=features):
            removed = []
            leaves = transformed_line.leaves
            last_index = len(leaves) - 1
            for i, leaf in enumerate(leaves):
                if leaf.type == token.ERRORTOKEN and leaf.value == ",":
                    if (i > 0 and leaves[i - 1].type == token.COMMA) or (
                        i < last_index and leaves[i + 1].type == token.COMMA
                    ):
                        removed.append(i)
            for i in removed[::-1]:
                del leaves[i]
            yield transformed_line

    def format_file_contents_patch(src_contents, *, fast, mode):
        try:
            return format_file_contents(src_contents, fast=fast, mode=mode)
        except AssertionError:
            return format_file_contents(
                _format_str_once(src_contents, mode=mode), fast=fast, mode=mode,
            )

    def has_magic_trailing_comma_patch(self, closing: Leaf) -> bool:
        if (
            (self.is_def or self.is_decorator)
            and closing.opening_bracket is not None
            and not is_one_sequence_between(closing.opening_bracket, closing, self.leaves)
        ):
            return True

        if closing.opening_bracket is None:
            return False

        # if already multiline, set multiline
        parent = self.leaves[-1].parent
        if parent.type not in (syms.arglist, syms.typedargslist):
            return False
        line = 0
        distinct_lines = 0
        for child in parent.children:
            if child.type == token.COMMA:
                if child.lineno != line:
                    line = child.lineno
                    distinct_lines += 1
        if distinct_lines <= 1:
            first_leaf = next(iter((parent.leaves())))
            comma_leaf = self.leaves[-1]
            assert comma_leaf.type == token.COMMA
            if first_leaf.lineno < line or comma_leaf.column in (0, self.mode.line_length):
                return False
            if line == closing.lineno:
                self.remove_trailing_comma()
            else:  # first_leaf.lineno == line
                comma_leaf.type = token.ERRORTOKEN
            return False

        return True

    black.format_file_contents = format_file_contents_patch
    black.transform_line = transform_line_patch
    black.linegen.transform_line = transform_line_patch
    Line.has_magic_trailing_comma_patch = has_magic_trailing_comma_patch

    func = Line.has_magic_trailing_comma
    code = func.__code__
    ops = bytearray(code.co_code)
    pattern = bytes(
        [
            dis.opmap["LOAD_FAST"],
            code.co_varnames.index("self"),
            dis.opmap["LOAD_ATTR"],
            code.co_names.index("is_import"),
            dis.opmap["POP_JUMP_IF_FALSE"],
        ],
    )
    pos = ops.find(pattern)
    assert pos >= 0, "patch failed for has_magic_trailing_comma"
    pos += len(pattern) + 5
    patch = [
        dis.opmap["LOAD_FAST"],
        code.co_varnames.index("self"),
        dis.opmap["LOAD_METHOD"],
        len(code.co_names),
        dis.opmap["LOAD_FAST"],
        code.co_varnames.index("closing"),
        dis.opmap["CALL_METHOD"],
        1,
        dis.opmap["RETURN_VALUE"],
    ]
    ops[pos : pos + len(patch)] = patch  # noqa: E203
    ops = ops[: pos + len(patch)]
    _patch_function(func, bytes(ops), code.co_names + ("has_magic_trailing_comma_patch",))

    return patched_main


def main():
    patch_black()()


if __name__ == "__main__":
    main()
