import os
import re
from typing import Iterator
from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest

from schemas import CmdEnums, RequestArgs

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def other_command(iter_obj: Iterator, query) -> Iterator:
    query_items = query.split('|')
    result = iter(map(str.strip, iter_obj))

    for item in query_items:
        cmd_value = item.split(':')
        command = cmd_value[0]

        value = cmd_value[0] if cmd_value[0] == 'unique' else cmd_value[1]

    return build_query(result, command, value)


def build_query(file_data: Iterator, cmd: str, value: str) -> Iterator:
    res = map(str.strip, file_data)

    if cmd == CmdEnums.filter:
        return filter(lambda v: value in v, res)
    elif cmd == CmdEnums.map:
        arg = int(value)
        return map(lambda v: v.split(" ")[arg], res)
    elif cmd == CmdEnums.unique:
        return set(res)
    elif cmd == CmdEnums.sort:
        return sorted(res, reverse=(value == "desc"))
    elif cmd == CmdEnums.limit:
        return list(res)[:int(value)]
    elif cmd == CmdEnums.regex:
        regex = re.compile(value)
        return filter(lambda v: regex.search(v), res)
    return res


@app.route("/perform_query", methods=["POST", "GET"])
def perform_query() -> Response:
    args: RequestArgs = RequestArgs().load(request.args)

    query = request.args.get("query")
    cmd1 = request.args.get("cmd1")
    cmd2 = request.args.get("cmd2")
    value1 = request.args.get("value1")
    value2 = request.args.get("value2")
    file_name = request.args.get("file_name")

    file_path = os.path.join(DATA_DIR, file_name)

    try:
        with open(file_path)as file:
            if query is not None:
                result = other_command(file, args.get("query"))
                content = '\n'.join(result)
            else:
                result = build_query(file, cmd1, value1)
                result = build_query(result, cmd2, value2)
                content = '\n'.join(result)
    except FileNotFoundError:
        return BadRequest(description=f"{file_name} was not found")

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)
