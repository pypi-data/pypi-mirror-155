from setuptools import setup, find_packages


setup(
	name='igc_reader',
	version='0.2.0',
	license='MIT',
	author='Douglas Brennan',
	author_email='douglas.brennan@me.com',
	packages=find_packages('src'),
	package_dir={'': 'src'},
	url='https://github.com/DouglasBrennan/igc_reader',
	keywords='igc reader',
	install_requires=[
		'pandas',
		'tqdm'
	],

)