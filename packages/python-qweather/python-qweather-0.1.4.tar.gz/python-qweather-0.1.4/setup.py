# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_qweather']

package_data = \
{'': ['*']}

install_requires = \
['pytest-asyncio>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'python-qweather',
    'version': '0.1.4',
    'description': 'Python API wrapper for https://qweather.com',
    'long_description': "# Python API wrapper for [和风天气](https://qweather.com)\n\n\n## Features\n- [城市信息查询](https://dev.qweather.com/docs/api/geo/city-lookup/)\n- [实时天气](https://dev.qweather.com/docs/api/weather/weather-now/)\n- [逐天天气预报](https://dev.qweather.com/docs/api/weather/weather-daily-forecast/)\n- [实时空气质量](https://dev.qweather.com/docs/api/air/air-now/)\n\n## Usage\n暂时只支持异步（async）调用，因为最初是为集成在 homeassistant 开发的 :)\n\n### 实时天气\n```python\nimport aiohttp\nimport asyncio\nfrom python_qweather import QWeather\n\nasync def test_now_weather():\n    async with aiohttp.ClientSession() as client_session:\n        q = QWeather(api_key=os.environ['QWEATHER_APIKEY'], session=client_session, location_key='101010100')\n        now_weather = await q.async_get_now_weather()\n        print(now_weather)\n\nasyncio.run(test_now_weather())\n```\n\n## TODO\n\n## Credits and Thanks\n- https://github.com/bieniu/accuweather\n",
    'author': 'dofine',
    'author_email': 'dofine@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dofine/python-qweather',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
