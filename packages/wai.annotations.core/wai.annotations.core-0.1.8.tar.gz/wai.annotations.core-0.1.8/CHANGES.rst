Changelog
=========

0.1.8 (2022-06-21)
------------------

- Added new audio domain for classification using suffix `-ac`
- Added dataset reader for audio files: `from-audio-files-sp`, `from-audio-files-ac`
- Added dataset writer for audio files: `to-audio-files-sp`, `to-audio-files-ac`
- Added dummy sink for audio files: `to-void-ac`
- Added ISP for selecting a sub-sample from the stream: `sample`


0.1.7 (2022-06-13)
------------------

- Added `discard-invalid-images` ISP for removing corrupt images or annotations with no image attached.
- Added `batch-split` sub-command for splitting individual batches of annotations into subsets like train/test/val.
  Supports grouping of files within batches (eg multiple images of the same object).
- Added `filter-metadata` ISP for filtering object detection.
- Restricted maximum characters per line in help output to 100 to avoid long help strings to become unreadable.
- The `polygon-discarder` now annotations that either have no polygon or invalid polygons.
- Added descriptions to the help screens of the main commands.
- The `ImageSegmentationAnnotation` class now outputs the unique values in its exception when there are
  more unique values than labels
- The `Data` class (module: `wai.annotations.core.domain`) now outputs a warning message if a file cannot
  be read; also added `LoggingEnabled` mixin.


0.1.6 (2022-05-11)
------------------

- Image segmentation annotations received new `label_images` property that returns images per
  label (as a dictionary); moved from the ToLayerSegments conversion (wai.annotations.layersegments)


0.1.5 (2022-05-09)
------------------

- Added dataset readers that generate dummy datasets from images: `from-images-ic`, `from-images-is`, `from-images-od`
- Added dataset writers that just output the images from datasets: `to-images-ic`, `to-images-is`, `to-images-od`

0.1.4 (2021-11-11)
------------------

- Added ISP for discarding polygons that either have too few or too many points (`polygon-discarder`)
- Added `--verbose` flag to `dimension-discarder` ISP for outputting information when an annotation
  gets discarded.

0.1.3 (2021-06-22)
-------------------

- Added cross-domain converter which reduces object-detection datasets to image classification
  by looking for single/majority objects/labels.

0.1.2 (2021-06-01)
-------------------

- Added void output formats for each domain which discard the conversion results.
- Added option to LocalFilenameSource which tells it to write the files it reads to a list-file.

0.1.1 (2021-05-20)
-------------------

- Fixed build.

0.1.0 (2021-05-20)
-------------------

- Initial release after separation from wai.annotations main repo.
