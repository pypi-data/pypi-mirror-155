import json
import os
from dataclasses import dataclass

from datagen import modalities
from datagen.components.datapoint.entity import base


@dataclass
class DataPoint(base.DataPoint):
    @modalities.textual_modality
    def actor_metadata(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="actor_metadata", file_name="actor_metadata.json")

    @modalities.textual_modality
    def face_bounding_box(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="face_bounding_box", file_name="face_bounding_box.json")

    @modalities.textual_modality
    def keypoints(self) -> modalities.TextualModality:
        return self._get_keypoints_v2() if self._use_keypoints_v2() else self._get_keypoints_v1()

    def _get_keypoints_v1(self) -> modalities.TextualModality:
        self._handle_keypoints_v1()
        return modalities.TextualModality(factory_name="keypoints", file_name="keypoints.json")

    def _get_keypoints_v2(self) -> modalities.TextualModality:
        return modalities.TextualModality(
            factory_name="keypoints", file_name=os.path.join("key_points", "all_key_points.json")
        )

    def _use_keypoints_v2(self) -> bool:
        v2_all_keypoints_file_path = self.camera_path.joinpath("key_points", "all_key_points.json")
        return v2_all_keypoints_file_path.exists()

    def _handle_keypoints_v1(self) -> None:
        keypoints_v1_file_path = self.camera_path.joinpath("keypoints.json")
        if not keypoints_v1_file_path.exists():
            self._create_keypoints_v1_file()

    def _create_keypoints_v1_file(self) -> None:
        with self.camera_path.joinpath("keypoints.json").open("w+") as keypoints_v1_file:
            standard_keypoints = json.loads(self.camera_path.joinpath("standard_keypoints.json").read_text())
            dense_keypoints = json.loads(self.camera_path.joinpath("dense_keypoints.json").read_text())
            json.dump({"standard": standard_keypoints, "dense": dense_keypoints}, keypoints_v1_file)
