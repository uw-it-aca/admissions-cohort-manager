<template>
  <div>
    <div v-if="show_error">
      No collections found for selected admissions period.
    </div>
    <div v-if="collectionType === 'Cohort'">
      <b-table
        v-if="show_error === false"
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :busy="is_loading"
        :items="cohorts"
        :fields="cohortFields"
        sort-by="value"
      >
        <template #cell(actions)="row">
          <a :href="'/cohort/' + row.item.value" :title="'Assign applications to cohort ' + row.item.value">Assign</a>
          <b-button size="sm" :title="'Remove all assignments to cohort ' + row.item.value" @click="handle_reset_button(row.item, row.index, $event.target)">
            Reset
          </b-button>
        </template>
        <template #table-busy>
          <div class="text-center text-info">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>

    <div v-else-if="collectionType === 'Major'">
      <b-table
        v-if="show_error === false"
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :busy="is_loading"
        :items="majors"
        :fields="majorFields"
        sort-by="value"
      >
        <template #cell(actions)="row">
          <a :href="'/major/' + row.item.value" :title="'Assign applications to major ' + row.item.value">Assign</a>
          <b-button size="sm" :title="'Remove all assignments to major' + row.item.value" @click="handle_reset_button(row.item, row.index, $event.target)">
            Reset
          </b-button>
        </template>
        <template #table-busy>
          <div class="text-center text-info">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>

    <div v-else>
      Error: There was an issue with your request. Please select a link from the left column to try again.
    </div>

    <!-- Reset Collection modal -->
    <reset-modal
      v-if="show_reset_modal"
      :key="modal_key"
      :collection-type="collectionType"
      :item-id="resetModal.itemId"
      :protected-cohort="resetModal.protect"
      v-on="$listeners"
    />
  </div>
</template>

<script>
  const axios = require("axios");
  import { EventBus } from "../main";
  import ResetModal from "../components/reset_modal";
  export default {
    name: "CollectionList",
    components: {
      ResetModal
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        cohortFields: [
          {
            key: 'value',
            label: "Cohort #",
            class: "aat-data-cell aat-data-nowrap center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'description',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'residency',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'protected',
            label: 'Protected',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'admit_decision',
            class: "aat-data-cell aat-data-nowrap center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'assigned_count',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          { key: 'actions',
            label: '',
            class: "aat-actions-cell aat-data-cell aat-data-nowrap", },
        ],
        cohorts: [],
        majorFields: [
          {
            key: 'value',
            label: 'Major Code',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'text',
            label: 'Major',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'division',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'college',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'dtx',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'assigned_count',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'Actions',
            label: '',
            class: "aat-actions-cell aat-data-cell aat-data-nowrap",
            sortable: false,
          }
        ],
        majors: [],
        show_reset_modal: false,
        resetModal: {
          id: 'reset-modal',
          title: '',
          itemId: '',
          ok_disabled: true,
          protect: false,
          timestamp: 0
        },
        checked: false,
        comment: '',
        admissions_period: null,
        is_loading: true,
        show_error: false,
        is_resetting: false
      };
    },
    computed: {
      modal_key: function () {
        return this.resetModal.itemId + this.resetModal.timestamp;
      }
    },
    watch: {
      checked: function(val){
        if(val === false){
          this.resetModal.ok_disabled = true;
        } else {
          this.resetModal.ok_disabled = false;
        }
      }
    },
    mounted() {
      this.setCSRF();
    },
    created(){
      this.admissions_period = this.$attrs.admissions_period;
      this.load_data();
      EventBus.$on('period-change', period => {
        this.admissions_period = period;
        this.load_data();
      });
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      load_data(){
        var vue = this;
        this.is_loading = true;
        this.show_error = false;
        axios.get(
          '/api/collection/'
            + this.collectionType.toLowerCase()
            + "/"
            + this.admissions_period
            + "/",
        ).then(response => {
          if(this.collectionType.toLowerCase() === "cohort"){
            this.cohorts = response.data;
          } else if (this.collectionType.toLowerCase() === "major"){
            this.majors = response.data;
          }
          this.is_loading = false;
        }).catch(function () {
          vue.show_error = true;
        });
      },
      handle_reset_button(item) {
        this.resetModal.itemId = `${item.value}`;
        this.resetModal.protect = (`${item.protected}` === 'true');
        this.resetModal.timestamp = Date.now();
        this.show_reset_modal = true;
      }
    }
  };
</script>

<style lang="scss">

  @import '../../css/_variables.scss';

  // Table action buttons
  .aat-actions-cell a,
  .aat-actions-cell button {
    color: $link-blue;
    font-family: 'Encode Sans Compressed',sans-serif;
    font-weight: bold;
    margin: 0 0.25rem;
    text-transform: uppercase;
  }

  .aat-actions-cell a i {
    color: $text-color;

    &:hover,
    &:focus {
      color: $link-blue;
    }
  }

  .aat-actions-cell.aat-data-cell .btn-secondary {
    background: none;
    border-style: none;
    color: $sub-header;
    font-size: 0.875rem;
    min-width: auto;
    padding: 0;
    vertical-align: baseline;

    &:hover,
    &:focus {
      color: $link-blue !important;
      text-decoration: underline;
    }
  }

</style>
