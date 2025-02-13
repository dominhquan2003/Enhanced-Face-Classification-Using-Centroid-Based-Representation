import { ScrollView, View, Image, Text, Modal, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useNavigation } from 'expo-router';
import { useEffect, useState } from 'react';
import styles from './detail.style'

import AntDesign from '@expo/vector-icons/AntDesign';
const PerformerDetail = () => {
  const { id } = useLocalSearchParams();
  const navigation = useNavigation();
  const [performer, setPerformer] = useState<any>(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedImage, setSelectedImage] = useState('');
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const response = await fetch(`${apiUrl}${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin": "*",
          }
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setPerformer(data);
        navigation.setOptions({ title: data.name });
      } catch (error) {
        console.error("Error fetching performer:", error);
      }
    };

    fetchDetail();
  }, [id]);


  if (!performer) return <Text>No performer found</Text>;


  const openModal = (imageUri : string) => {
    setSelectedImage(imageUri);
    setModalVisible(true);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.row}>
        <TouchableOpacity onPress={() => openModal(performer.original_image)}>
          <View style={styles.imageContainer}>
            <Image source={{ uri: performer.original_image }} style={styles.imageLarge} />
            <Text style={styles.label}>Original Image</Text>
          </View>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => openModal(performer.detected_image)}>
          <View style={styles.imageContainer}>
            <Image source={{ uri: performer.detected_image }} style={styles.imageLarge} />
            <Text style={styles.label}>Input Image heat map</Text>
          </View>
        </TouchableOpacity>
      </View>

      <View style={styles.row}>
        <TouchableOpacity onPress={() => openModal(performer.heatmap_1)}>
          <View style={styles.imageContainer}>
            <Image source={{ uri: performer.heatmap_1 }} style={styles.imageSmall} />
            <Text style={styles.label}>Predict Actor 1</Text>
          </View>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => openModal(performer.heatmap_2)}>
          <View style={styles.imageContainer}>
            <Image source={{ uri: performer.heatmap_2 }} style={styles.imageSmall} />
            <Text style={styles.label}>Predict Actor 2</Text>
          </View>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => openModal(performer.heatmap_3)}>
          <View style={styles.imageContainer}>
            <Image source={{ uri: performer.heatmap_3 }} style={styles.imageSmall} />
            <Text style={styles.label}>Predict Actor 3</Text>
          </View>
        </TouchableOpacity>
      </View>

   
      <Modal
        visible={modalVisible}
        transparent={true}
        animationType="slide"
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeIconCover}>
            <AntDesign name="closecircleo" style={styles.closeIcon}  />
           
          </TouchableOpacity>
          <Image source={{ uri: selectedImage }} style={styles.modalImage} />
        </View>
      </Modal>
    </ScrollView>
  );


};


export default PerformerDetail;
