import { StyleSheet } from 'react-native';
import color from '../../contains/color'
const styles = StyleSheet.create({
      container: {
            flex: 1,
            backgroundColor: color.background,
      },
      body: {
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center'
      },
      bodyWrapper: {
            width: "70%",
            aspectRatio: 1,
            borderWidth: 2,
            borderColor: color.badge2,
            borderStyle: 'dashed',
            borderRadius: 20,
            justifyContent: 'center',
            alignItems: 'center'
      },
      addTag: {
            fontSize: 100,
            fontWeight: 'bold',
            color: color.badge2
      },
      iconWrapper: {
            position: 'absolute',
            bottom: 20,
            right: 20,
            height: 44,
            width: 44,
            backgroundColor: color.badge2,
            borderRadius: 22,
            justifyContent: "center",
            alignItems: "center",
            borderWidth: 2,
            borderColor: color.badge2,
            elevation: 5,
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 2 },
            shadowOpacity: 0.3,
            shadowRadius: 4,
      },
      icon: {
            color: color.white,
            fontSize: 24,
            zIndex: 1,
      },

      addTagForm: {
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
            borderColor: color.badge2,
            backgroundColor: color.white,
            paddingHorizontal: 14,
            paddingVertical: 10,
      },
      postWrapper: {
            height: 44,
            width: 44,
            backgroundColor: color.badge2,
            borderRadius: 22,
            justifyContent: "center",
            alignItems: "center",
            borderWidth: 2,
            borderColor: color.badge2,

      },
      post: {
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
      imageContainer: {
            position: 'relative',
            width: '100%',
            height: '100%',
            overflow: 'hidden',
      },
      imagePreview: {
            position: 'absolute',
            width: '100%',
            height: '100%',
            borderRadius: 20,
            resizeMode: 'cover',
            zIndex: 1,
      },
      removeIcon: {
            position: 'absolute',
            top: 5,
            right: 5,
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
            borderRadius: 15,
            padding: 5,
            zIndex: 2,
      },
      iconClose: {
            fontSize: 20,
            color: 'red',
      },

      dropdownBtn: {
            marginTop: 10,
            width: '50%',
            height: 50,
            backgroundColor: color.background,
            borderWidth: 1,
            borderColor: color.badge2,
            borderRadius: 8,
            justifyContent: 'space-between',
            paddingHorizontal: 10,
            flexDirection: 'row',
            alignItems: 'center',

      },
      dropdown: {
            backgroundColor: '#FFF',
            borderRadius: 8,
            marginTop: 5,
            elevation: 5,
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 2 },
            shadowOpacity: 0.2,
            shadowRadius: 4,

      },
      rowText: {
            padding: 10,
            fontSize: 16,
            color: '#333',

      },
      buttonText: {
            color: "#888", // Màu chữ trắng cho giá trị mặc định
            fontSize: 16, // Kích thước chữ
      },
});
export default styles;
