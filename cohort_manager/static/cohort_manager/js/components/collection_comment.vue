<template>
  <fieldset class="aat-form-section">
    <legend class="aat-sub-header">
      Add Comment
    </legend>
    <label for="assignment_comment">Enter comment for this assignment</label>
    <textarea id="assignment_comment" v-model="comment" class="aat-comment-field" />
  </fieldset>
</template>

<script>
  export default {
    name: "CollectionComment",
    components: {
    },
    data() {
      return {
        comment: ''
      };
    },
    watch: {
      comment(){
        this.$emit('comment', this.comment);
      }
    },
    methods: {
    }
  };
</script>

<style lang="scss">
  .aat-comment-field {
    display: block;
    height: 144px;
    max-width: 650px;
    min-width: 250px;
    padding: 0.5rem;
    width: 100%;
  }
</style>
