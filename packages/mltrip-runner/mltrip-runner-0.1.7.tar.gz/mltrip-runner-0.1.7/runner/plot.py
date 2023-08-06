import argparse
from pathlib import Path

from pyvis.network import Network

from runner.run import initialize
from runner.factory import Factory
from runner.load import load


def plot_action(a, output_path=None, height='600px', width='600px', title="",
                options=False, no_hierarchy=False,
                background='white', font='black'):
    if output_path is None:
        if a.tag is not None:
            output_path = a.tag + '.html'
        else:
            output_path = a.uid + '.html'
    routes = a.get_routes()
    a2route = {v: k for k, v in routes.items()}
    graph = a.get_graph()
    n = Network(height=height, width=width, heading=title,
                directed=True, bgcolor=background, font_color=font)

    def get_class(action):
        cls = action.__class__
        return cls.__module__ + '.' + cls.__qualname__

    def make_title(action):
        title = f"""
        route: {a2route.get(action, None)}<br>
        class: {get_class(action)}<br>
        tag: {action.tag}<br>
        jobs: {action.jobs}<br>
        delay: {action.delay}<br>
        timeout: {action.timeout}<br>
        executor: {action.executor}<br>
        routine: {action.routine}<br>
        workers: {action.workers}<br>"""
        return title

    executor2color = {None: 'blue',
                      'ThreadPoolExecutor': 'red',
                      'ProcessPoolExecutor': 'green'}
    executor2title = {None: 'Sequence',
                      'ThreadPoolExecutor': 'Thread',
                      'ProcessPoolExecutor': 'Process'}
    nodes, edges, groups = set(), set(), {}
    for p, cs in graph.items():
        if p not in nodes:
            n.add_node(p.uid,
                       label=p.tag if p.tag is not None else ' ',
                       group=groups.setdefault(get_class(p), len(groups)),
                       title=make_title(p))
            nodes.add(p)
        for c in cs:
            if c not in nodes:
                n.add_node(c.uid,
                           label=c.tag if c.tag is not None else ' ',
                           group=groups.setdefault(get_class(c), len(groups)),
                           title=make_title(c))
                nodes.add(c)
            if (p, c) not in edges:
                n.add_edge(p.uid, c.uid,
                           title=executor2title[p.executor],
                           color=executor2color[p.executor])
                edges.add((p, c))
    if options:
        n.show_buttons()
    else:
        if not no_hierarchy:
            n.set_options("""
            var options = {
              "layout": {
                "hierarchical": {
                    "enabled": true,
                    "direction": "LR",
                    "sortMethod": "directed"
                    }
                }
            }
            """)
    n.write_html(str(Path(output_path)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='input')
    parser.add_argument('-o', '--output_path', help='output', default=None)
    parser.add_argument('--height', help='height', default='100%')
    parser.add_argument('--width', help='width', default='100%')
    parser.add_argument('--title', help='title', default='')
    parser.add_argument('--background', help='background color', default='white')
    parser.add_argument('--font', help='font color', default='black')
    parser.add_argument('--options', help='show options', action='store_true')
    parser.add_argument('--no_hierarchy', help='non hierarchical layout', action='store_true')
    args = vars(parser.parse_known_args()[0])  # arguments dictionary
    p = Path(args['input_path'])
    d = load(p)
    d.setdefault('metadata', {})
    d.setdefault('data', {})
    f = Factory()
    a = initialize(d['data'], f)
    if args['output_path'] is None:
        args['output_path'] = p.with_suffix('.html')
    args.pop('input_path')
    plot_action(a, **args)


if __name__ == '__main__':
    main()
