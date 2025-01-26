import { StyleSheet } from 'react-native';
import color from '../../contains/color'
const styles = StyleSheet.create({
      addTag: {
            bottom: 30,
            paddingHorizontal: 20,
            width: "100%",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
      },
      input: {
            height: 44,
            width: "80%",
            borderWidth: 2,
            borderRadius: 20,
            borderColor: color.primary,
            backgroundColor: color.white,
            paddingHorizontal: 14,
            paddingVertical: 10,
      },
      iconWrapper: {
            height: 44,
            width: 44,
            backgroundColor: color.primary,
            borderRadius: 22,
            justifyContent: "center",
            alignItems: "center",
            borderWidth: 2,
            borderColor: color.primary,

      },
      icon: {
            color: color.white,
            fontSize: 24,
      },
      selectedImage: {
            height: 100,
            width: 100,
            borderRadius: 12,
            marginBottom: 32,
            marginLeft: 10,
            zIndex: 1, 
          },
});
export default styles;
