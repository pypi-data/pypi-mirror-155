from importlib import import_module

from tsdl.common import util
from tsdl.core.context import Context
from tsdl.logger.log import logger


def handle(context: Context):
    model = import_module(context.script)
    sorted_steps_no, steps = extract_steps_from_model(dir(model))

    index = 0

    while index < len(sorted_steps_no):
        step_no = sorted_steps_no[index]

        if meet_loops(context, int(step_no)):
            index = loop_steps(context, model, steps, index)
        else:
            exec_step(context, model, steps.get(step_no))
            context.runtime.reset_loop()

        index += 1


def extract_steps_from_model(steps: list):
    n_s = []
    m_d = {}
    for s in steps:
        if s.upper().find('STEP_') >= 0:
            n = util.extract_digit(s)
            n_s.append(n)
            m_d[n] = s

    sorted_n_s = sorted(n_s)

    return sorted_n_s, m_d


def meet_loops(context: Context, step_no):
    try:
        lp = context.loops[0]
        if lp is None:
            return False
    except IndexError as e:
        return False

    if lp.range.start <= step_no <= lp.range.end:
        return True

    return False


def loop_steps(context: Context, model, steps: dict, index: int):
    lp = context.loops.pop(0)
    blank = 0

    logger.info('~ &LOOPS START -step_range {}-{} -count {}'.format(lp.range.start, lp.range.end, lp.count))
    context.runtime.loop_total_times = lp.count
    for i in range(lp.count):
        logger.info('~ &&LOOP start to run no.{}, total.{} '.format(i + 1, lp.count))
        blank = 0
        for j in range(lp.range.start, lp.range.end + 1):
            step = steps.get(str(j))
            if step is not None:
                exec_step(context, model, step)
            else:
                blank += 1
        context.runtime.loop_times = i + 1
    logger.info('~ &LOOPS END.')

    return index + (lp.range.end - lp.range.start) - blank


def exec_step(context: Context, model, step: str):
    logger.info('~ #{}# start to run'.format(step.upper()))
    context.runtime.step = step

    result = getattr(model, '{}'.format(step))(context)
    if result is not None:
        context.runtime.last_result = result

