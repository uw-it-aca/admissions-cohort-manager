<template>
  <b-container class="aat-details-container aat-form-section" fluid>
    <b-row>
      <b-col class="aat-group-info-primary">
        <b-row class="aat-info-spacing">
          <b-col cols="2" class="aat-data-primary">
            Major
            <div class="aat-group-data aat-data-primary">
              {{ majorData.abbr }}
            </div>
          </b-col>
          <b-col cols="6" class="aat-group-info-secondary">
            Description
            <div class="aat-group-data aat-data-baseline">
              {{ majorData.text }}
            </div>
          </b-col>
          <b-col cols="4" class="aat-group-info-secondary">
            Major Program Code
            <div class="aat-group-data aat-data-baseline">
              {{ majorData.major_id }}
            </div>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
    <b-row class="aat-group-info-secondary">
      <b-col class="aat-info-spacing">
        College <div class="aat-group-data">
          {{ majorData.college }}
        </div>
      </b-col>
      <b-col class="aat-info-spacing">
        Division <div class="aat-group-data">
          {{ majorData.division }}
        </div>
      </b-col>
      <b-col class="aat-info-spacing">
        DTX<div class="aat-group-data">
          {{ majorData.dtx }}
        </div>
      </b-col>
      <b-col class="aat-info-spacing">
        Assigned
        <div class="aat-group-data">
          {{ majorData.applications_assigned }}
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  export default {
    name: "MajorDetails",
    components: {},
    props: {
      majorData: {
        type: Object,
        default() {
          return {};
        }
      }
    },
    data(){
      return {
      };
    },
    watch: {
      collectionId: function() {
        this.collection_id = this.collectionId;
        this.get_collection();
      },
      collectionData: {
        handler: function(){
          this.collection_data = this.collectionData;
          this.process_collection_data();
        },
        deep: true
      },
      collection_data: {
        handler: function(){
          this.process_collection_data();
        },
        deep: true
      }
    },
    created () {
    },

    methods: {
    },
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';

  // general layout
  .aat-form-section {
    &.aat-details-container {
      border: solid $banner-border 1px;
      color: $sub-header;
      font-size: 0.85rem;
      line-height: 1.5;
      margin: 0.5rem 0 1.5rem;
      max-width: 650px;
      padding: 2rem;
    }
  }

  // labels and data

  .aat-group-info-primary {
    .aat-group-data {
      font-size: 2rem;

    }
  }

  .aat-group-data {
    color: $text-color;
    font-weight: bold;
  }

  .aat-info-spacing {
    padding-bottom: 1.5rem;
  }

  .aat-group-info-secondary {
    .row {
      align-items: unset;
      flex-direction: column;
      font-weight: normal;
      margin: 0 auto;
      padding: 0 25%;
    }

    .aat-group-data {
      font-size: 1rem;
      font-weight: normal;
    }

    .aat-info-spacing {
      padding-bottom: 1rem;
    }
  }

  // small screen overrides
  @media screen and (max-width: 767px) {
    .aat-group-info-primary {
      margin-bottom: 2rem;
    }

    .aat-group-info-secondary {
      margin-bottom: 1rem;
    }

  }

</style>
