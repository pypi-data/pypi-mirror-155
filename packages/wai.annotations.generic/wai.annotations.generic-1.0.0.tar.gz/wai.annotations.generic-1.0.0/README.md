# wai-annotations-generic
wai.annotations module to make it easier to plugin custom code into a wai.annotations pipeline.

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins

### GENERIC-SOURCE-AC
Generic audio classification source.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: generic-source-ac [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SOURCE-IC
Generic image classification source.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: generic-source-ic [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SOURCE-IS
Generic image segmentation source.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: generic-source-is [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```

### GENERIC-SOURCE-OD
Generic object detection source.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: generic-source-od [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SOURCE-SP
Generic speech source.

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: generic-source-sp [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-ISP-AC
Generic audio classification ISP.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: generic-isp-ac [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-ISP-IC
Generic image classification ISP.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: generic-isp-ic [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-ISP-IS
Generic image segmentation ISP.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: generic-isp-is [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-ISP-OD
Generic object detection ISP.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: generic-isp-od [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-ISP-SP
Generic speech ISP.

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: generic-isp-sp [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SINK-AC
Generic audio classification sink.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: generic-sink-ac [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SINK-IC
Generic image classification sink.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: generic-sink-ic [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SINK-IS
Generic image segmentation sink.

#### Domain(s):
- **Image Segmentation Domain**

#### Options:
```
usage: generic-sink-is [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SINK-OD
Generic object detection sink.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: generic-sink-od [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


### GENERIC-SINK-SP
Generic speech sink.

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: generic-sink-sp [-c USER_CLASS] [-o USER_OPTIONS]

optional arguments:
  -c USER_CLASS, --class USER_CLASS
                        the user class to wrap (dot notation) (default: None)
  -o USER_OPTIONS, --options USER_OPTIONS
                        the options for the user class to parse (default: None)
```


## Examples

The following examples have the test classes linked for guidance on developing your own plugins.

### Audio classification

* [Source](src/wai/annotations/generic/source/audio_classification/test/_TestAC.py)
  ```bash
  wai-annotations convert \
    generic-source-ac \
      -c wai.annotations.generic.source.audio_classification.test.TestAC \
      -o "--dir /some/where/" \  # dir with .wav files
    generic-sink-ac \
      -c wai.annotations.generic.sink.audio_classification.test.TestAC \
      -o "--output label"
  ```

* [ISP](src/wai/annotations/generic/isp/audio_classification/test/_TestAC.py)
  ```bash
  wai-annotations convert \
    from-audio-files-ac \
      -i "/some/where/*.wav" \
    generic-isp-ac \
      -c wai.annotations.generic.isp.audio_classification.test.TestAC \
      -o "--output filename" \
    to-void-ac
  ```

* [Sink](src/wai/annotations/generic/sink/audio_classification/test/_TestAC.py)
  ```bash
  wai-annotations convert \
    from-audio-files-ac \
      -i "/some/where/*.wav" \
    generic-sink-ac \
      -c wai.annotations.generic.sink.audio_classification.test.TestAC \
      -o "--output filename"
  ```

### Image classification

* [Source](src/wai/annotations/generic/source/image_classification/test/_TestIC.py)
  ```bash
  wai-annotations convert \
    generic-source-ic \
      -c wai.annotations.generic.source.image_classification.test.TestIC \
      -o "--dir /some/where/" \  # dir with .jpg files
    generic-sink-ic \
      -c wai.annotations.generic.sink.image_classification.test.TestIC \
      -o "--output label"
  ```
  
* [ISP](src/wai/annotations/generic/isp/image_classification/test/_TestIC.py)
  ```bash
  wai-annotations convert \
    from-images-ic \
      -i "/some/where/*.jpg" \
    generic-isp-ic \
      -c wai.annotations.generic.isp.image_classification.test.TestIC \
      -o "--output dimensions" \
    to-void-ic
  ```

* [Sink](src/wai/annotations/generic/sink/image_classification/test/_TestIC.py)
  ```bash
  wai-annotations convert \
    from-images-ic \
      -i "/some/where/*.jpg" \
    generic-sink-ic \
      -c wai.annotations.generic.sink.image_classification.test.TestIC \
      -o "--output dimensions"
  ```

### Image segmentation

* [Source](src/wai/annotations/generic/source/image_segmentation/test/_TestIS.py)
  ```bash
  wai-annotations convert \
    generic-source-is \
      -c wai.annotations.generic.source.image_segmentation.test.TestIS \
      -o "--labels A B C --dir /some/where/" \    # dir with .jpg files
    generic-sink-is \
      -c wai.annotations.generic.sink.image_segmentation.test.TestIS \
      -o "--output dimensions"

  ```

* [ISP](src/wai/annotations/generic/isp/image_segmentation/test/_TestIS.py)
  ```bash
  wai-annotations convert \
    from-images-is \
      -i "/some/where/*.jpg" \
    generic-isp-is \
      -c wai.annotations.generic.isp.image_segmentation.test.TestIS \
      -o "--output dimensions" \
    to-void-is
  ```

* [Sink](src/wai/annotations/generic/sink/image_segmentation/test/_TestIS.py)
  ```bash
  wai-annotations convert \
    from-images-is \
      -i "/some/where/*.jpg" \
    generic-sink-is \
      -c wai.annotations.generic.sink.image_segmentation.test.TestIS \
      -o "--output dimensions"
  ```

### Object Detection

* [Source](src/wai/annotations/generic/source/object_detection/test/_TestOD.py)
  ```bash
  wai-annotations convert \
    generic-source-od \
      -c wai.annotations.generic.source.object_detection.test.TestOD \
      -o "--dir /some/where/" \   # dir with .jpg files
    generic-sink-od \
      -c wai.annotations.generic.sink.object_detection.test.TestOD \
      -o "--output num_objects"
  ```

* [ISP](src/wai/annotations/generic/isp/object_detection/test/_TestOD.py)
  ```bash
  wai-annotations convert \
    from-images-od \
      -i "/some/where/*.jpg" \
    generic-isp-od \
      -c wai.annotations.generic.isp.object_detection.test.TestOD \
      -o "--output dimensions" \
    to-void-od
  ```

* [Sink](src/wai/annotations/generic/sink/object_detection/test/_TestOD.py)
  ```bash
  wai-annotations convert \
    from-images-od \
      -i "/some/where/*.jpg" \
    generic-sink-od \
      -c wai.annotations.generic.sink.object_detection.test.TestOD \
      -o "--output dimensions"
  ```

### Speech

* [Source](src/wai/annotations/generic/source/speech/test/_TestSP.py)
  ```bash
  wai-annotations convert \
    generic-source-sp \
      -c wai.annotations.generic.source.speech.test.TestSP \
      -o "--dir /some/where/" \  # dir with .wav files
    generic-sink-ac \
      -c wai.annotations.generic.sink.speech.test.TestSP \
      -o "--output label"
  ```

* [ISP](src/wai/annotations/generic/isp/speech/test/_TestSP.py)
  ```bash
  wai-annotations convert \
    from-audio-files-sp \
      -i "/some/where/*.wav" \
    generic-isp-sp \
      -c wai.annotations.generic.isp.speech.test.TestSP \
      -o "--output filename" \
    to-void-sp
  ```

* [Sink](src/wai/annotations/generic/sink/speech/test/_TestSP.py)
  ```bash
  wai-annotations convert \
    from-audio-files-sp \
      -i "/some/where/*.wav" \
    generic-sink-sp \
      -c wai.annotations.generic.sink.speech.test.TestSP \
      -o "--output filename"
  ```
