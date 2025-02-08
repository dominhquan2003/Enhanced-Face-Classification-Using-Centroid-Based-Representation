import { View, Text, TextInput, Alert, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import styles from './style';
import React, { useState } from 'react';
import AntDesign from '@expo/vector-icons/AntDesign';
import { ImageHandler } from './imageHandler';
import { handlePost } from './handlePost';



const Form = () => {
  const [performerName, setPerformerName] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const handleImageUpload = async () => {
    await ImageHandler.handleUploadImage(setSelectedImage);
  }
  const onPostSuccess = () => {
    // Logic sau khi post thành công
    setPerformerName('');
  };

  const submitHandler = () => {
    handlePost(performerName, onPostSuccess);
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.body}>
        <TouchableOpacity style={styles.bodyWrapper} onPress={handleImageUpload}>
          <AntDesign name="camera" style={styles.addTag} />
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
