import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gd-vae-pytorch",
    version="1.0.1",
    author="Ryan Lopez and Paul J. Atzberger",
    author_email="atzberg@gmail.com",
    description="Implementation of GD-VAEs for PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://atzberger.org/",
    packages=['gd_vae_pytorch', 'gd_vae_pytorch.tests'],
    #packages=setuptools.find_packages(include=['gd-vae-pytorch']),
    #setup_requires=["numpy>=1.16","scipy>=1.3","matplotlib>=3.0"],
    #install_requires=["numpy>=1.16","scipy>=1.3","matplotlib>=3.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# print a message after install 
##ss="";
#ss+="PyTorch implementation of GD-VAEs.\n";
#ss+="\n"
#ss+="NOTE: The package is still being packaged for pip. \n";
#ss+="Please sign-up below for Google-Form for mailing list \n";
#ss+="announcing soon this code release: \n";
#ss+="https://forms.gle/mJSRRrqMo8CwFKRC7 \n";
#ss+="\n";
#ss+="Additional information also can be found at: \n";
#ss+="http://atzberger.org \n";
#
#print(ss);


