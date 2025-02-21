import React from 'react';
import { router, Stack } from 'expo-router';
import color from '../contains/color';
import { TouchableOpacity, View } from 'react-native';
import Feather from '@expo/vector-icons/Feather';
import styles from './App.component.style';
import { TaskProvider } from '../context/TaskContext';
const Layout = () => {
  return (
    <TaskProvider>
      <Stack screenOptions={{ headerTitleStyle: { fontWeight: 'bold', color: color.primary } }}>
        <Stack.Screen
          name="index"
          options={{
            title: 'LIST OF PERFORMERS',
            headerRight: () => (
              <TouchableOpacity onPress={() => router.push('/add-performer')}>
                <View style={{ paddingVertical: 12 }}>
                  <Feather name="user-plus" style={styles.icon} />
                </View>
              </TouchableOpacity>
            ),
          }}
        />
        <Stack.Screen name="add-performer" options={{ title: 'Add Performer' }} />
      </Stack>
    </TaskProvider>

  );
};

export default Layout;