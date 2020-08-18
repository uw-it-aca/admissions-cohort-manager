<template>
  <iframe_base v-if="isFrame" />
  <full_base v-else />
</template>

<script>
  import FullBase from './full_base';
  import iFrameBase from "./iframe_base";

  export default {
    name: "Base",
    components: {
      full_base: FullBase,
      iframe_base: iFrameBase
    },
    data(){
      return {
      };
    },
    computed: {
      isFrame() {
        return this.$route.path.includes("iframe");
      }
    },
    watch: {
    },
    mounted() {
    },
    methods: {

    }
  };
</script>

<style lang="scss">
</style>
