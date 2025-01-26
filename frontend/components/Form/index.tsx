import { View, Text, TextInput, Alert, TouchableOpacity, KeyboardAvoidingView, Platform, Image } from 'react-native';
import styles from './style';
import React, { useState } from 'react';
import Ionicons from '@expo/vector-icons/Ionicons';
import { ImageHandler } from './imageHandler';

const Form = () => {

      // const [performerName, setPerformerName] = useState('');
      // const handlePost = async () => {
      //       try {
      //             const response = await fetch('http://127.0.0.1:8000/facedetect/api/v1/', {
      //                   method: 'POST',
      //                   headers: {
      //                         'Content-Type': 'application/json',
      //                   },
      //                   body: JSON.stringify({ name: performerName }),
      //             });
      //             if (!response.ok) {
      //                   throw new Error(`HTTP error! status: ${response.status}`);
      //             }                  
      //             const data = await response.json();
      //             console.log('Success:', data);
      //             // Xử lý phản hồi...
      //       } catch (error) {
      //             console.error('Error:', error);
      //       }
      // };
      return (
            <View>
                  {/* <View>
                        {selectedImage && (
                              <Image source={{ uri: selectedImage }} style={styles.selectedImage} />
                        )}
                  </View> */}
                  <KeyboardAvoidingView
                        behavior={Platform.OS === "ios" ? 'padding' : 'height'}
                        style={styles.addTag}
                        keyboardVerticalOffset={10}
                  >
                        <TextInput
                              style={styles.input}
                              placeholder="Name of performer"
                             
                        />
                        {/* <TouchableOpacity onPress={onPressImage}>
                              <View style={styles.iconWrapper}>
                                    <Ionicons name="camera" size={24} color="white" />
                              </View>
                        </TouchableOpacity> */}
                        <TouchableOpacity>
                              <View style={styles.iconWrapper}>
                                    <Text style={styles.icon}>+</Text>
                              </View>
                        </TouchableOpacity>
                  </KeyboardAvoidingView>
            </View>
      );
};

export default Form;