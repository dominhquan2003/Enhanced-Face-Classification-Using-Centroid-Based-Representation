from nbconvert import PythonExporter
import nbformat

# Đọc notebook
with open('d:/TailieuhocTDTu/ProjectInformationTechnology/reactnative_mobileapp/backendapi/api/test.ipynb', 'r', encoding='utf-8') as f:
    notebook_content = nbformat.read(f, as_version=4)

# Chuyển đổi
exporter = PythonExporter()
py_content, _ = exporter.from_notebook_node(notebook_content)

# Ghi ra file .py
with open('d:/TailieuhocTDTu/ProjectInformationTechnology/reactnative_mobileapp/backendapi/api/predict.py', 'w', encoding='utf-8') as f:
    f.write(py_content)