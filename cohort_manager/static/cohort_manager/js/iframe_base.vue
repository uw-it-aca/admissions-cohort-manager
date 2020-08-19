<template>
  <div>
    <p>IFRAME BASE</p>
    <main ref="main" aria-labelledby="aat_page_header" class="col aat-main-container">
      <router-view />
    </main>
  </div>
</template>

<script>

  export default {
    name: "IFrameBase",
    components: {
    },
    data(){
      return {
      };
    },
    computed: {
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
