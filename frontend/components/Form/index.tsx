import { View, Text, TextInput, Alert, TouchableOpacity, KeyboardAvoidingView, Platform, Image } from 'react-native';
import styles from './style';
import React, { useState } from 'react';
import AntDesign from '@expo/vector-icons/AntDesign';
import { ImageHandler } from './imageHandler';
import { handlePost } from './handlePost';
import { useTaskContext } from '../../context/TaskContext'; // Import hook


const Form = () => {
  const [performerName, setPerformerName] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const { addTask } = useTaskContext(); 
  const handleImageUpload = async () => {
    await ImageHandler.handleUploadImage(setSelectedImage);
  }
  const onPostSuccess = () => {
    setPerformerName('');
    setSelectedImage(null);
  };

  const submitHandler = () => {
    if (performerName.trim() === "") {
      Alert.alert("Error", "Please provide a performer name.");
      return;
    } else if (!selectedImage) {
      Alert.alert("Error", "Please provide an image.");
      return;
    }
    handlePost(performerName, selectedImage, onPostSuccess,addTask);
  };
  const removeImage = () => {
    setSelectedImage(null); // Reset selected image
  };
  return (
    <View style={styles.container}>
      <View style={styles.body}>
        <TouchableOpacity style={styles.bodyWrapper} onPress={handleImageUpload}>

          {selectedImage && (
            <Image
              source={{ uri: selectedImage }}
              style={styles.imagePreview} // Style for the image
            />
          )}
          <AntDesign name="camera" style={styles.addTag} />
          {selectedImage && (
            <TouchableOpacity style={styles.removeIcon} onPress={removeImage}>
              <AntDesign name="close" style={styles.iconClose} />
            </TouchableOpacity>
          )}

        </TouchableOpacity>

      </View>
      <View >
        <KeyboardAvoidingView
          behavior={Platform.OS === "ios" ? 'padding' : 'height'}
          style={styles.addTagForm}
          keyboardVerticalOffset={10}
        >
          <TextInput
            style={styles.input}
            placeholder="Name of performer"
            value={performerName}
            onChangeText={setPerformerName}
          />
          <TouchableOpacity onPress={submitHandler}>
            <View style={styles.postWrapper}>
              <AntDesign name="arrowup" style={styles.post} />

            </View>
          </TouchableOpacity>
        </KeyboardAvoidingView>
      </View>


    </View>


  );
};

export default Form;
