"""Unit-level prerequisites and project-focused route expansion."""

def index_units(modules):
    return {n['id']: n for m in modules for n in m['nodes']}


def sort_key(unit_id):
    return tuple(int(x) for x in unit_id.split('.'))


def topological_units(modules):
    units = index_units(modules)
    pending = {k: set(n['prerequisites']) for k,n in units.items()}
    unknown = set().union(*pending.values()) - units.keys()
    if unknown:
        raise ValueError('Unknown prerequisites: '+', '.join(sorted(unknown)))
    done = set()
    ordered = []
    while pending:
        ready = sorted((k for k,v in pending.items() if v <= done), key=sort_key)
        if not ready:
            raise ValueError('Unit prerequisite cycle: '+', '.join(sorted(pending)))
        done.update(ready)
        ordered.extend(ready)
        pending = {k:v for k,v in pending.items() if k not in done}
    return ordered


def expand_route(modules, route, include_optional=False):
    units = index_units(modules)
    topological_units(modules)
    done = set()
    stages = []
    def visit(unit_id, added):
        if unit_id in done:
            return
        if unit_id not in units:
            raise ValueError('Unknown route unit: '+unit_id)
        for prerequisite in units[unit_id]['prerequisites']:
            visit(prerequisite, added)
        done.add(unit_id)
        added.append(unit_id)
    for stage in route['stages']:
        if stage.get('optional') and not include_optional:
            stages.append({**stage, 'units': [], 'skipped_optional': True})
            continue
        added = []
        for unit_id in stage['targets']:
            visit(unit_id, added)
        stages.append({**stage, 'units': added})
    return stages
