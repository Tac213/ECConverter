import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ListView {
    id: root
    required property string imageSource
    spacing: 9
    highlight: Rectangle {
        color: "lightsteelblue"
        radius: 5
    }
    delegate: Item {
        required property string path
        height: 40
        width: ListView.view.width
        RowLayout {
            anchors.fill: parent
            spacing: 9
            Image {
                Layout.preferredHeight: 40
                Layout.preferredWidth: 40
                fillMode: Image.PreserveAspectFit
                mipmap: true
                source: root.imageSource  // qmllint disable unqualified
            }
            Text {
                text: parent.parent.path  // qmllint disable type
                font.pointSize: 15
                horizontalAlignment: Text.AlignLeft
                Layout.alignment: Qt.AlignLeft
                Layout.fillWidth: true
            }
        }
    }
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: event => {
            root.currentIndex = root.indexAt(event.x, event.y);
            if (event.button == Qt.RightButton) {
                contextMenu.popup();
            }
        }
    }
    Menu {
        id: contextMenu
        MenuItem {
            action: deleteAction
        }
        MenuItem {
            action: clearAction
        }
    }
    Action {
        id: deleteAction
        text: qsTr("删除")
        enabled: root.currentIndex !== -1
        onTriggered: () => {
            root.deleteItem(root.currentIndex);
        }
    }
    Action {
        id: clearAction
        text: qsTr("清空")
        onTriggered: () => {
            root.clear();
        }
    }
    Component.onCompleted: () => {
        this.currentIndex = -1;
    }

    function clear() {
        this.model.deserialize([]);
    }

    function deleteItem(index) {
        const modelIndex = this.model.index(index, 0);
        this.model.remove_node(modelIndex);
        this.currentIndex = -1;
    }

    function addItem(path) {
        const parentIndex = this.model.index(-1, -1);
        this.model.add_node(parentIndex, path);
    }

    // animations
    add: Transition {
        NumberAnimation {
            properties: "y"
            from: root.height
            duration: 500
        }
    }
    addDisplaced: Transition {
        NumberAnimation {
            properties: "x,y"
            duration: 500
        }
    }
    displaced: Transition {
        NumberAnimation {
            properties: "x,y"
            duration: 500
        }
    }
    move: Transition {
        NumberAnimation {
            properties: "x,y"
            duration: 500
        }
    }
    moveDisplaced: Transition {
        NumberAnimation {
            properties: "x,y"
            duration: 500
        }
    }
    populate: Transition {
        NumberAnimation {
            properties: "x,y"
            duration: 500
        }
    }
    remove: Transition {
        ParallelAnimation {
            NumberAnimation {
                property: "opacity"
                to: 0
                duration: 500
            }
            NumberAnimation {
                properties: "y"
                to: 0
                duration: 500
            }
        }
    }
    removeDisplaced: Transition {
        NumberAnimation {
            properties: "x,y"
            duration: 500
        }
    }
}
