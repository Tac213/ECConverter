import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "CommonComponents" as CommonComponents
import Python.ItemListModel  // qmllint disable import
import Python.FileUrlHelper  // qmllint disable import
import Python.SettingsHelper  // qmllint disable import
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
                    model: enumModel
                    imageSource: "qrc:/resource/opened_folder.png"
                    anchors.fill: parent
                }
            }
        }
        Button {
            id: selectEnumButton
            Layout.fillWidth: true
            display: AbstractButton.TextOnly
            text: qsTr("选择Enum")
            onClicked: () => {
                enumFolderDialog.visible = true;
            }
        }
        RowLayout {
            Layout.fillWidth: true
            spacing: 9
            Button {
                id: convertButton
                Layout.fillWidth: true
                display: AbstractButton.TextOnly
                text: qsTr("导出Enum")
                onClicked: () => {
                    const currentEnums = enumModel.serialize();
                    if (currentEnums.length === 0) {
                        return;
                    }
                    const success = converter.convert_enum(currentEnums, dataValidationCheckBox.checked);
                    if (success) {
                        root.showSuccessDialog(qsTr('导出Enum成功'));
                    } else {
                        root.showFailureDialog(qsTr('导出Enum失败, 失败原因参照输出窗口'));
                    }
                }
            }
            CheckBox {
                id: dataValidationCheckBox
                checked: true
                text: qsTr("是否生成数据验证")
            }
        }
        Button {
            id: genInfoButton
            Layout.fillWidth: true
            display: AbstractButton.TextOnly
            text: qsTr("生成项目Enum信息")
            onClicked: () => {
                const success = converter.generate_enum_info();
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
        id: enumModel
    }
    FileUrlHelper {
        id: fileUrlHelper
    }
    SettingsHelper {
        id: settingsHelper
    }
    Converter {
        id: converter
    }
    // qmllint enable import type
    FolderDialog {
        id: enumFolderDialog
        title: qsTr("选择需要导出的Enum")
        currentFolder: fileUrlHelper.excel_dir()  // qmllint disable type
        onAccepted: {
            const currentEnums = enumModel.serialize();
            const excelDir = fileUrlHelper.excel_dir();
            const enumURL = this.selectedFolder.toString();
            if (!enumURL.includes(excelDir)) {
                console.warn(qsTr(`所选Enum目录'${enumURL}'不在目录'${excelDir}'内`));
                return;
            }
            const enumRelpath = enumURL.substring(excelDir.length + 1);
            if (currentEnums.includes(enumRelpath)) {
                return;
            }
            const enumInfo = settingsHelper.enum_info();
            if (!(enumRelpath in enumInfo)) {
                console.warn(qsTr(`所选Enum目录必须在这些目录内: ${Object.keys(enumInfo)}`));
                return;
            }
            listView.addItem(enumRelpath);
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
        return enumModel.serialize();  // qmllint disable type
    }

    function deserialize(data) {
        enumModel.deserialize(data);  // qmllint disable type
    }
}
