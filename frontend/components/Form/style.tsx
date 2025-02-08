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
});
export default styles;
