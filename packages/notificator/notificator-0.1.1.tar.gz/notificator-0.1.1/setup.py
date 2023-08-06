from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent

setup(
    name='notificator',
    version='0.1.1',
    keywords=['notice', 'notificator', 'bark', 'sms', 'mail'],
    description='Central Notification',
    long_description='send sms, bark, or mail message via notice.6-79.cn',
    long_description_content_type='text/markdown',
    license='MIT Licence',
    url='https://github.com/Jyonn/CentralNotificationSDK',
    author='Jyonn Liu',
    author_email='i@6-79.cn',
    platforms='any',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
