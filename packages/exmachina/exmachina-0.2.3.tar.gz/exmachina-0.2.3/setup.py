# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['exmachina', 'exmachina.core', 'exmachina.lib']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.10.0,<4.0.0']

extras_require = \
{'rich': ['rich>=10.1.0,<11.0.0']}

setup_kwargs = {
    'name': 'exmachina',
    'version': '0.2.3',
    'description': 'botを作るためのフレームワークです',
    'long_description': '# Ex-Machina\n\n<p align="center">\n  <em>python で bot 書くためのフレームワーク</em>\n</p>\n<p align="center">\n<a href="https://github.com/agarichan/exmachina/actions/workflows/test.yaml" target="_blank">\n  <img src="https://github.com/agarichan/exmachina/actions/workflows/test.yaml/badge.svg?branch=main" alt="Test">\n</a>\n<a href="https://codecov.io/gh/agarichan/exmachina" target="_blank">\n  <img src="https://img.shields.io/codecov/c/github/agarichan/exmachina?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/exmachina" target="_blank">\n  <img src="https://img.shields.io/pypi/v/exmachina?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/exmachina" target="_blank">\n  <img src="https://img.shields.io/pypi/pyversions/exmachina.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n---\n\n## インストール\n\nusing pip\n\n```\npip install -U exmachina\n```\n\nusing poetry\n\n```\npoetry add exmachina@latest\n```\n\n## 使い方\n\n\n```python\nimport asyncio\n\nfrom exmachina import Event, Machina, Retry, RetryFixed\n\nbot = Machina()\n\nbot.create_concurrent_group(\n    name=\'limit\',\n    entire_calls_limit=4,\n    time_calls_limit=3,\n    time_limit=1,\n)\n\n@bot.emit(interval=\'1s\')\nasync def emit(event: Event):\n    res = await event.execute(\'execute\')\n    assert res == 42\n    # or\n    res = await execute()\n    assert res == 42\n\n# 特定の例外でリトライしたい場合\nretry = Retry([\n  RetryFixed(HTTPError, wait_time=1, retries=5),\n])\n\n@bot.execute(concurrent_groups=[\'limit\'], retry=retry)\nasync def execute():\n    return 42\n\nif __name__ == "__main__":\n    try:\n        wasyncio.run(bot.run())\n    except KeyboardInterrupt:\n        print("終了")\n```\n\n### Emit\n\n定期的に実行したい関数を登録するためのデコレータ\n\n- `name`\n  - Emitでユニークな名前をつける\n  - 省略した場合はデコレートした関数名になる\n- `count`\n  - 実行回数. これで指定した回数実行した後、`alive`が`False`になる\n  - `None`を指定した場合は無限回実行する\n  - デフォルトは`None`\n- `interval`\n  - ループのインターバル `1s`や`1d4h`などと指定できる\n  - デフォルトは`0s`. つまり待機しない\n- `alive`\n  - `True`の場合、botの実行時に自動で実行される\n  - 手動で起動する場合は`False`を指定する\n  - デフォルトは`True`\n\n### Concurrent Group\n\n時間あたりや同時実行数を制限するグループ  \n作成したグループは後述のExecuteに対して設定できる\n\n- `name`\n  - 必須プロパティ. Concurrent Groupでユニークな名前をつける\n- `entire_calls_limit`\n  - 全体の実行数制限\n  - このグループに所属するExecuteの並列実行数\n  - `None`を指定した場合、無制限\n  - デフォルトは`None`\n- `time_calls_limit`\n  - このグループに所属する`time_limit`秒あたりに実行"開始"できるExecuteの数\n  - デフォルトは`1`\n- `time_limit`\n  - `time_calls_limit`の制限時間(秒)\n  - デフォルト`0`. つまり、制限なし\n\n### Execute\n\nEmitから呼び出される、一回きりのタスク  \nEmitは主にbotの制御を行い、Executeは計算処理や外部との通信を行う処理を書く想定\n\n- `name`\n  - Executeでユニークな名前をつける\n  - 省略した場合はデコレートした関数名になる\n- `concurrent_groups`\n  - executeの所属するconcurrent_groupを配列で指定する\n  - デフォルトは`[]`\n- `retry`\n  - Execute実行中に発生した例外をトリガーにリトライを行う設定を指定する\n  - `from exmachina import Retry`\n  - デフォルトは`None`\n\n## Event\n\nEmitする関数に渡されるオブジェクト\n\n- 停止中の別のEmit起動や停止\n- Executeの実行\n- ループの状態を確認できる属性を持つ\n\n### Emitの起動と停止\n\n```python\nevent.start(\'emit_name\')\nevent.stop(\'emit_name\')\n```\n\n### Executeの実行\n\n```python\nevent.execute(\'execute_name\', *args, **kwargs)\n```\n\nまたは、直接呼び出し\n\n```python\nawait execute_name(*args, **kwargs)\n````\n\nevent.executeはexecuteのTaskを返す\n\n### 属性\n\n```python\nevent.epoch # emitのループ回数\nevent.previous_execution_time # 直前のループの処理時間\nevent.count # emitの残りの実行回数(未指定の場合はNone)\n```\n\n## Retry\n\nExecuteのリトライの設定を書くためのもの  \n特定の秒数を待機した後、そのまま再実行を行う\n\n- `rules`\n  - 指定するルールの配列\n- `logger`\n  - 自前のloggerを渡したい場合に使う\n\n### RetryRule\n\n- `RetryFixed`: 常に`wait_time`の間隔でリトライ\n- `RetryFibonacci`: 1,1,2,3,5,...とフィボナッチ数列秒の間隔でリトライ\n- `RetryRange`: `min`と`max`を指定し、その間の乱数秒の間隔でリトライ\n- `RetryExponentialAndJitter`: 指数関数倍的に最大の待機時間を伸ばしつつリトライ\nのいずれかを使用する\n\n共通引数\n- `exception`\n  - 指定する例外のクラス\n- `retries`\n  - リトライ回数. 省略すると`RecursionError`が出るまで再実行する\n  - デフォルトは`None`\n- `filter`\n  - 例外インスタンスを引数に`bool`を返す関数を指定\n  - Trueを返した場合にこのリトライ条件にマッチする\n  - HTTPのステータスコードなどで引っ掛けたいリトライ設定が異なる場合などを想定\n  - デフォルトは`None`. つまり、常に`True`を返す\n## 開発\n\n### init\n\n```bash\npoetry install\npoetry shell\n```\n\n### fmt\n\n```\npoe fmt\n```\n\n### lint\n\n```\npoe lint\n```\n\n### test\n\n```\npoe test\n```\n',
    'author': 'agarichan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agarichan/exmachina',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
