from setuptools import setup, find_packages

setup(
    name='infocircle',
    packages=find_packages(),
    include_package_data=True,
    version="1.0.0",
    description='RPBI CIRCLE ID TO INFORMATION',
    author='AKXVAU',
    author_email='akxvau@gmail.com',
    long_description=(open("README.md","r")).read(),
    long_description_content_type="text/markdown",
   install_requires=['requests', 'lolcat'],
 
    keywords=['hacker','blsms', 'spam', 'tool', 'sms', 'pyenc', 'call', 'prank', 'termux', 'hack','Py Encrypt','Encryptor', 'AKXVAU','ROBI','CORCLE','ROBI CIRCLE', 'INFOCIRCLE'],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'blotp = blotp.blotp:menu',
                
            ],
    },
    python_requires='>=3.9'
)
