import asyncio
import logging
import traceback
from asyncio import StreamReader, FIRST_EXCEPTION
from datetime import datetime, timezone, timedelta
from subprocess import PIPE, STDOUT, Popen
from typing import List, Tuple, Optional, Dict, TypeAlias, Callable

from dateutil.parser import parse as dateutil_parse


def dump_rfc3339(dt: datetime) -> str:
    assert dt.tzinfo is not None  # enforce timezone aware (non-naive) datetime
    dt = dt.replace(microsecond=0)  # not interested in sub second precision
    res = dt.isoformat()
    if res.endswith("+00:00"):
        # +00:00 is nicer to write as Z (Zulu timezone)
        # But both are valid.
        res = res[:-6] + "Z"
    return res


def parse_rfc3339(date_str: str) -> datetime:
    # dateutil_parse parses ISO 8601, which contains almost all of RFC3339. This is good enough.
    res = dateutil_parse(date_str)
    assert res.tzinfo is not None  # assert timezone aware (non-naive) datetime
    return res


def datetime_now(zulu=False, no_milliseconds=True) -> datetime:
    res = datetime.now(timezone.utc)
    if not zulu:
        res = res.astimezone(timezone(timedelta(hours=0), name="UTC"))
    if no_milliseconds:
        res = res.replace(microsecond=0)
    assert res.tzinfo is not None  # enforce timezone aware (non-naive) datetime
    return res


def call_external_command_sync(*params: str, **kwargs) -> Tuple[int, str]:
    res = ""
    com: List[str] = list(params)
    kwargs["stdout"] = PIPE
    kwargs["stderr"] = STDOUT
    kwargs["universal_newlines"] = True
    with Popen(com, **kwargs) as proc:
        for line in proc.stdout:
            res += line
        res_code = proc.wait()
        # if res_code != 0:
        #     raise Exception('Command returned error ({}): {} (command={} )'.format(res_code, res.strip(), com))
        return res_code, res.strip()


OutputHandler: TypeAlias = Callable[[str], None]
NO_OUTPUT = lambda msg: None


async def log_output(out: OutputHandler, stream: StreamReader):
    saw_eof = False
    while not saw_eof:
        line = await stream.readline()
        if line:
            out(line.decode())
        else:
            saw_eof = True


async def call_external_command_async(
    *,
    command: List[str],
    cwd: Optional[str] = None,
    env: Dict[str, str] = {},
    timeout_s=3600,
    stdout_handler: OutputHandler = NO_OUTPUT,
    stderr_handler: OutputHandler = NO_OUTPUT,
    debug_log_handler: OutputHandler = NO_OUTPUT,
    error_log_handler: OutputHandler = NO_OUTPUT,
) -> int:
    # await add_log(
    #     perftest_id,
    #     LogLevel.DEBUG,
    #     f"Will run command: {command!r} with env={env} in cwd={cwd}",
    #     session=session,
    # )
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
        env=env,
    )
    tasks = []
    stdout_log_task = asyncio.create_task(log_output(stdout_handler, proc.stdout))
    stderr_log_task = asyncio.create_task(log_output(stderr_handler, proc.stderr))
    tasks.append(stdout_log_task)
    tasks.append(stderr_log_task)
    proc_done_task = asyncio.create_task(proc.wait())
    tasks.append(proc_done_task)

    pre_wait = datetime_now()

    debug_log_handler(
        f"Started command. Will wait for up to {timeout_s} seconds. Starting at {pre_wait}"
    )

    done, pending = await asyncio.wait(
        tasks,
        timeout=timeout_s,
        return_when=FIRST_EXCEPTION,
    )
    post_wait = datetime_now()
    logging.debug(
        f"(pre_wait={pre_wait} post_wait={post_wait}) len(done)={len(done)} len(pending)={len(pending)}"
    )
    if pending:
        saw_exception = False
        for d in done:
            e = d.exception()
            if e:
                saw_exception = True
                logging.error("Saw exception waiting", exc_info=e)
                tb = "".join(traceback.format_exception(None, e, e.__traceback__))
                error_log_handler(
                    f"Command exception: Will be cancelled. "
                    f"(pre_wait={pre_wait} post_wait={post_wait} e={e} {tb})",
                )
        if not saw_exception:
            error_log_handler(
                f"Command did not return within {timeout_s} seconds: Will be cancelled. "
                f"(pre_wait={pre_wait} post_wait={post_wait})",
            )
        for p in pending:
            p.cancel()
            proc.kill()
        return -1
    else:
        debug_log_handler(
            f"Command exited with exitcode {proc.returncode}",
        )
        return proc.returncode
