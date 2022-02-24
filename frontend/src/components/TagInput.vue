<template>
  <div class="tag-input">
    <div class="field has-addons">
      <div class="control">
        <!-- <div class="dropdown"> -->
        <div
          class="dropdown"
          v-bind:class="{ 'is-active': tag_dropdown_active }"
        >
          <div class="dropdown-trigger">
            <button
              class="button"
              aria-haspopup="true"
              aria-controls="dropdown-menu"
              v-on:click="tag_dropdown_active = !tag_dropdown_active"
            >
              <span class="icon is-small">
                <i class="v-md-icon-arrow-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a
                class="dropdown-item is-success"
                v-for="(tag, index) in tags"
                :key="tag"
              >
                <button
                  class="delete is-small"
                  @click="removeTag(index)"
                ></button>
                {{ tag }}
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="control">
        <input
          class="input is-primary"
          placeholder="タグを追加"
          v-model="newTag"
          type="text"
          :list="id"
          autocomplete="off"
          @keydown.enter="addTag(newTag)"
          @keydown.prevent.tab="addTag(newTag)"
          @keydown.delete="newTag.length || removeTag(tags.length - 1)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { watch, ref, onMounted, nextTick } from "vue";
export default {
  name: "TagInput",
  props: {
    modelValue: { type: Array, default: () => [] },
    tag_dropdown_active: false,
  },
  setup(props, { emit }) {
    // Tags
    const tags = ref(props.modelValue);
    const newTag = ref("");
    const id = Math.random().toString(36).substring(7);
    const addTag = (tag) => {
      if (!tag) return; // prevent empty tag
      // return early if duplicate
      if (tags.value.includes(tag)) {
        handleDuplicate(tag);
        return;
      }
      tags.value.push(tag);
      newTag.value = ""; // reset newTag
      // console.log("modelValue:", props.modelValue);
      // console.log("ref tags:", tags);
    };
    const removeTag = (index) => {
      tags.value.splice(index, 1);
    };
    const duplicate = ref(null);
    const handleDuplicate = (tag) => {
      duplicate.value = tag;
      setTimeout(() => (duplicate.value = null), 1000);
      newTag.value = "";
    };
    const onTagsChange = () => {
      // emit value on tags change
      emit("update:modelValue", tags.value);
    };
    watch(tags, () => nextTick(onTagsChange), { deep: true });
    onMounted(onTagsChange);
    return {
      tags,
      newTag,
      addTag,
      removeTag,
      id,
      duplicate,
    };
  },
};
</script>