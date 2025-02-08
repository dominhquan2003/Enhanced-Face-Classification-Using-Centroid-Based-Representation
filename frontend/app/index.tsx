import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import Task from '../components/Task';
import styles from '../app/App.component.style';

export default function HomeScreen() {


  return (
    <View style={styles.container}>
      <View style={styles.body}>
        <Task/>
      </View>
      <StatusBar style="auto" />
    </View>
  );
}