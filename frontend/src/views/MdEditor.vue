<template>
  <div style="text-align: left">
    <v-md-editor
      v-model="text"
      left-toolbar="undo redo | h changecolor bold italic strikethrough quote textalignleft textaligncenter textalignright | ul ol table hr | link image code | tip todo-list | save"
      height="500px"
      :include-level="[1, 2]"
      :toolbar="toolbar"
    />
  </div>
</template>

<script>
export default {
  name: "MdEditor",
  data() {
    const text = "";
    this.toolbar = {
      changecolor: {
        title: "change color",
        icon: "v-md-custom-icon-color",
        menus: {
          mode: "panel",
          itemWidth: "56px",
          rowNum: 5,
          items: [
            {
              text: "red",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: red; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
            {
              text: "blue",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: blue; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
            {
              text: "green",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: green; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
            {
              text: "yellow",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: yellow; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
          ],
        },
      },
      textalignleft: {
        title: "text align left",
        icon: "v-md-custom-icon-align-left",
        action(editor) {
          editor.insert(function (selected) {
            const prefix = ":::align-left\n";
            const suffix = "\n:::";
            const placeholder = "placeholder";
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
      textaligncenter: {
        title: "text align center",
        icon: "v-md-custom-icon-align-center",
        action(editor) {
          editor.insert(function (selected) {
            const prefix = ":::align-center\n";
            const suffix = "\n:::";
            const placeholder = "placeholder";
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
      textalignright: {
        title: "text align right",
        icon: "v-md-custom-icon-align-right",
        action(editor) {
          editor.insert(function (selected) {
            const prefix = ":::align-right\n";
            const suffix = "\n:::";
            const placeholder = "placeholder";
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
    };
    return {
      text: text,
    };
  },
};
</script>