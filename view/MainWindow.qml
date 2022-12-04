import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import Python.FileUrlHelper  // qmllint disable import
import Python.FileIOHelper  // qmllint disable import
import "script/const.js" as Const

ApplicationWindow {
    id: root

    title: qsTr("ECConverter")
    width: 1334
    height: 750
    minimumWidth: 1334
    minimumHeight: 750
    visible: true
    RowLayout {
        anchors.fill: parent
        Page {
            id: selectWindow
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumWidth: 300
            header: TabBar {
                id: selectWindowTabBar
                width: parent.width
                TabButton {
                    text: qsTr("导出Excel")
                    width: implicitWidth
                }
                TabButton {
                    text: qsTr("导出Enum")
                    width: implicitWidth
                }
            }
            StackLayout {
                anchors.fill: parent
                currentIndex: selectWindowTabBar.currentIndex
                SelectExcel {
                    id: selectExcel
                }
                SelectEnum {
                    id: selectEnum
                }
            }
        }
        OutputWindow {
            id: consoleWindow
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.maximumWidth: 800
        }
    }
    // qmllint disable import type
    FileIOHelper {
        id: fileIOHelper
    }
    FileUrlHelper {
        id: fileUrlHelper
    }
    // qmllint enable import type
    onClosing: () => {
        const rootDir = fileUrlHelper.root_dir();
        const storageFileURL = `${rootDir}/${Const.localStorageFileName}`;
        const storageData = {
            "remember_last_excels": true,
            "last_excels": selectExcel.serialize(),
            "remember_last_enums": true,
            "last_enums": selectEnum.serialize()
        };
        const storageDataString = JSON.stringify(storageData);
        fileIOHelper.write_text_file(storageFileURL, 'utf-8', storageDataString);
    }

    Component.onCompleted: () => {
        console.info(qsTr('第一步: 选择需要导表的Excel'));
        console.info(qsTr('第二步: 点击导表按钮, 开始导表'));
        const rootDir = fileUrlHelper.root_dir();
        const storageFileURL = `${rootDir}/${Const.localStorageFileName}`;
        const storageDataString = fileIOHelper.read_text_file(storageFileURL, 'utf-8');
        if (!storageDataString) {
            return;
        }
        const storageData = JSON.parse(storageDataString);
        if ('last_excels' in storageData) {
            selectExcel.deserialize(storageData['last_excels']);
        }
        if ('last_enums' in storageData) {
            selectEnum.deserialize(storageData['last_enums']);
        }
    }
}
