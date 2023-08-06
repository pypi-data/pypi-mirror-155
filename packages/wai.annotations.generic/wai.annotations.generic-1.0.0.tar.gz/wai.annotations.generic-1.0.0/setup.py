from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.generic",
    description="Module with generic plugins for wai.annotations that use user specified classes.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-datamining/wai-annotations-generic",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations"
    ],
    version="1.0.0",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "wai.annotations.core>=0.1.7"
    ],
    entry_points={
        "wai.annotations.plugins": [
            # Sources
            "generic-source-ac=wai.annotations.generic.source.audio_classification.specifier:AudioClassificationSourceSpecifier",
            "generic-source-ic=wai.annotations.generic.source.image_classification.specifier:ImageClassificationSourceSpecifier",
            "generic-source-is=wai.annotations.generic.source.image_segmentation.specifier:ImageSegmentationSourceSpecifier",
            "generic-source-od=wai.annotations.generic.source.object_detection.specifier:ObjectDetectionSourceSpecifier",
            "generic-source-sp=wai.annotations.generic.source.speech.specifier:SpeechSourceSpecifier",
            # ISPs
            "generic-isp-ac=wai.annotations.generic.isp.audio_classification.specifier:AudioClassificationISPSpecifier",
            "generic-isp-ic=wai.annotations.generic.isp.image_classification.specifier:ImageClassificationISPSpecifier",
            "generic-isp-is=wai.annotations.generic.isp.image_segmentation.specifier:ImageSegmentationISPSpecifier",
            "generic-isp-od=wai.annotations.generic.isp.object_detection.specifier:ObjectDetectionISPSpecifier",
            "generic-isp-sp=wai.annotations.generic.isp.speech.specifier:SpeechISPSpecifier",
            # Sinks
            "generic-sink-ac=wai.annotations.generic.sink.audio_classification.specifier:AudioClassificationSinkSpecifier",
            "generic-sink-ic=wai.annotations.generic.sink.image_classification.specifier:ImageClassificationSinkSpecifier",
            "generic-sink-is=wai.annotations.generic.sink.image_segmentation.specifier:ImageSegmentationSinkSpecifier",
            "generic-sink-od=wai.annotations.generic.sink.object_detection.specifier:ObjectDetectionSinkSpecifier",
            "generic-sink-sp=wai.annotations.generic.sink.speech.specifier:SpeechSinkSpecifier",
        ]
    }
)
