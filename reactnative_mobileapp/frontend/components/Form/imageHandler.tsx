import React, { useState } from 'react';
import { Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export class ImageHandler {
  static async pickImage() {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false,
      quality: 1,
    });

    return result;
  }

  static async handleUploadImage(setSelectedImage: React.Dispatch<React.SetStateAction<string | null>>) {
    const result = await this.pickImage();
    if (result && !result.canceled && result.assets && result.assets.length > 0) {
      setSelectedImage(result.assets[0].uri);
    }
  }
}

