<template>
  <b-modal id="dupe_list_modal" ref="dupe_modal" title="Remove Dupes" ok-title="Done" @ok="removeDupes">
    <div>
      <p>This is the dupe modal</p>
      <b-card-text class="aat-sub-header">
        <h3>Select applications to assign</h3>
      </b-card-text>
      <b-card-text>
        <applicationlist
          application-return="Duplicate"
          :collection-type="collectionType"
          :applications="duplicates"
          @dupeToRemove="proc"
        />
      </b-card-text>
    </div>
  </b-modal>
</template>

<script>
  import ApplicationList from "../components/application_list.vue";
  export default {
    name: "CollectionUploadDupeModal",
    components: {
      applicationlist : ApplicationList
    },
    props: {
      duplicates: {
        type: Array,
        default: function () {return[];}
      },
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
      };
    },
    mounted() {
      this.$refs.dupe_modal.show();
    },
    methods: {
      proc: function(list){
        this.$emit("dupeToRemove", list);
      },
      removeDupes() {
        return;
      }
    }
  };
</script>

<style lang="scss">
</style>
