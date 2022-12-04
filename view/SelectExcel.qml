import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "CommonComponents" as CommonComponents
import Python.ItemListModel  // qmllint disable import
import Python.FileUrlHelper  // qmllint disable import
import Python.Converter  // qmllint disable import

Frame {
    id: root
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 9
        spacing: 9
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ScrollView {
                id: scrollView
                anchors.fill: parent
                anchors.margins: 9
                CommonComponents.ItemListView {
                    id: listView
                    model: excelModel
                    imageSource: "qrc:/resource/excel.png"
                }
            }
        }
        Button {
            id: selectExcelButton
            Layout.fillWidth: true
            display: AbstractButton.TextOnly
            text: qsTr("选择Excel")
            onClicked: () => {
                excelFileDialog.visible = true;
            }
        }
        Button {
            id: convertButton
            Layout.fillWidth: true
            display: AbstractButton.TextOnly
            text: qsTr("导表")
            onClicked: () => {
                const currentFiles = excelModel.serialize();
                if (currentFiles.length === 0) {
                    return;
                }
                const success = converter.convert_data(currentFiles);
                if (success) {
                    root.showSuccessDialog(qsTr('导表成功'));
                } else {
                    root.showFailureDialog(qsTr('导表失败, 失败原因参照输出窗口'));
                }
            }
        }
        Button {
            id: genInfoButton
            Layout.fillWidth: true
            display: AbstractButton.TextOnly
            text: qsTr("生成项目Excel信息")
            onClicked: () => {
                const success = converter.generate_excel_info();
                if (success) {
                    root.showSuccessDialog(qsTr('生成成功'));
                } else {
                    root.showFailureDialog(qsTr('生成失败, 失败原因参照输出窗口'));
                }
            }
        }
    }
    // qmllint disable import type
    ItemListModel {
        id: excelModel
    }
    FileUrlHelper {
        id: fileUrlHelper
    }
    Converter {
        id: converter
    }
    // qmllint enable import type
    FileDialog {
        id: excelFileDialog
        title: qsTr("选择需要导表的Excel")
        fileMode: FileDialog.OpenFiles
        nameFilters: ["Excel files (*.xlsx)"]
        currentFolder: fileUrlHelper.excel_dir()  // qmllint disable type
        onAccepted: {
            const currentFiles = excelModel.serialize();
            const excelDir = fileUrlHelper.excel_dir();
            for (let fileURL of this.selectedFiles) {
                fileURL = fileURL.toString();
                if (!fileURL.includes(excelDir)) {
                    console.warn(qsTr(`所选Excel文件'${fileURL}'不在目录'${excelDir}'内`));
                    continue;
                }
                const fileRelpath = fileURL.substring(excelDir.length + 1);
                if (fileRelpath.includes('/')) {
                    console.warn(qsTr(`所选Excel文件'${fileURL}'在目录'${excelDir}'的子目录内`));
                    continue;
                }
                if (currentFiles.includes(fileRelpath)) {
                    continue;
                }
                listView.addItem(fileRelpath);
            }
        }
    }
    MessageDialog {
        id: messageDialog
        buttons: MessageDialog.Ok  // qmllint disable type
        visible: false
    }

    function showSuccessDialog(text) {
        messageDialog.title = qsTr('提示');
        messageDialog.text = text;
        messageDialog.visible = true;
    }

    function showFailureDialog(text) {
        messageDialog.title = qsTr('错误');
        messageDialog.text = text;
        messageDialog.visible = true;
    }

    function serialize() {
        return excelModel.serialize();  // qmllint disable type
    }

    function deserialize(data) {
        excelModel.deserialize(data);  // qmllint disable type
    }
}
