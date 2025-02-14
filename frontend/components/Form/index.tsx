import { View, Text, TextInput, Alert, TouchableOpacity, KeyboardAvoidingView, Platform, Image } from 'react-native';
import styles from './style';
import React, { useState } from 'react';
import AntDesign from '@expo/vector-icons/AntDesign';
import { ImageHandler } from './imageHandler';
import { handlePost } from './handlePost';
import { useTaskContext } from '../../context/TaskContext';
import SelectDropdown from 'react-native-select-dropdown';

const Form = () => {
  const [performerName, setPerformerName] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const { addTask } = useTaskContext();
  const [kmeansValue, setKmeansValue] = useState('kmeans_k=16');


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
    handlePost(performerName, selectedImage, onPostSuccess, addTask, kmeansValue);
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
              style={styles.imagePreview}
            />
          )}
          <AntDesign name="camera" style={styles.addTag} />
          {selectedImage && (
            <TouchableOpacity style={styles.removeIcon} onPress={removeImage}>
              <AntDesign name="close" style={styles.iconClose} />
            </TouchableOpacity>
          )}

        </TouchableOpacity>

        <SelectDropdown
          data={['kmeans_k=16', 'kmeans_k=32']}
          onSelect={(selectedItem, index) => {
            const kmeansValue = selectedItem.replace('kmeans_k=', '');
            setKmeansValue(kmeansValue); // Lưu dưới dạng chuỗi
          }}
          defaultValue={kmeansValue ? `kmeans_k=${kmeansValue}` : "Select KMeans"}// Hiển thị giá trị mặc định
          renderButton={(selectedItem, isOpened) => {
            return (
              <TouchableOpacity style={styles.dropdownBtn}>
                <Text style={styles.buttonText}>{selectedItem || "Select KMeans"}</Text>
                <AntDesign style={styles.buttonText} name={isOpened ? "caretup" : "caretdown"} />
              </TouchableOpacity>
            );
          }}
          renderItem={(item, index) => {
            return (
              <TouchableOpacity key={index} onPress={() => setKmeansValue(item)}>
                <Text style={styles.rowText}>{item}</Text>
              </TouchableOpacity>
            );
          }}
          dropdownStyle={styles.dropdown} // Kiểu cho dropdown
          showsVerticalScrollIndicator={false} // Không hiển thị chỉ báo cuộn

        />

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
