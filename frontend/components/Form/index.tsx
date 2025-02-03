import { View, Text, TextInput, Alert, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import styles from './style';
import React, { useState } from 'react';

// Thêm kiểu cho prop
interface FormProps {
  onPostSuccess: () => void;
}

const Form = ({ onPostSuccess }: FormProps) => {
  const [performerName, setPerformerName] = useState('');

  const handlePost = async () => {
    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({
        name: performerName,
        status: true,
        original_image: null,
        detected_image: null,
        heatmap_1: null,
        heatmap_2: null,
        heatmap_3: null
      }),
    };

    try {
      const response = await fetch('http://10.66.2.113:8000/facedetect/api/v1/', requestOptions);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Success:', data);
      Alert.alert('Success', 'Performance added successfully!');
      setPerformerName('');
      
      // Gọi callback để thông báo về việc post thành công
      onPostSuccess(); 
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <View>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? 'padding' : 'height'}
        style={styles.addTag}
        keyboardVerticalOffset={10}
      >
        <TextInput
          style={styles.input}
          placeholder="Name of performer"
          value={performerName}
          onChangeText={setPerformerName}
        />
        <TouchableOpacity onPress={handlePost}>
          <View style={styles.iconWrapper}>
            <Text style={styles.icon}>+</Text>
          </View>
        </TouchableOpacity>
      </KeyboardAvoidingView>
    </View>
  );
};

export default Form;
