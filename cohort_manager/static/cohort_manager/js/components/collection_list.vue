<template>
  <div>
    <div v-if="collectionType === 'Cohort'">
      <b-table
        striped
        show-empty
        small
        class="aat-data-table"
        :items="cohorts"
        :fields="cohortFields"
      >
        <template v-slot:cell(actions)="row">
          <a href="/cohort/" :title="'Assign applications to cohort ' + row.item.name">Assign</a>
          <a href="/log/" :title="'Activity for cohort ' + row.item.name"><i class="far fa-clock" /><span class="sr-only">Activity</span></a>
          <a href="www.tableau.com" :title="'View cohort ' + row.item.name + ' in Tableau'"><i class="fas fa-external-link-alt" /><span class="sr-only">View cohort in Tableau</span></a>
          <b-button size="sm" :title="'Remove all assignments to cohort ' + row.item.name" @click="info(row.item, row.index, $event.target)">
            Reset
          </b-button>
        </template>
      </b-table>
    </div>

    <div v-else-if="collectionType === 'Major'">
      <b-table
        striped
        show-empty
        small
        class="aat-data-table"
        :items="majors"
        :fields="majorFields"
      >
        <template v-slot:cell(actions)="row">
          <a href="/major/" :title="'Assign applications to major ' + row.item.name">Assign</a>
          <a href="/log/" :title="'Activity for major ' + row.item.name"><i class="far fa-clock" /><span class="sr-only">Activity</span></a>
          <b-button size="sm" :title="'Remove all assignments to major' + row.item.name" @click="info(row.item, row.index, $event.target)">
            Reset
          </b-button>
        </template>
      </b-table>
    </div>

    <div v-else>
      Error: There was an issue with your request. Please select a link from the left column to try again.
    </div>

    <!-- Reset Collection modal -->
    <template>
      <div>
        <b-modal :id="resetModal.id" :title="resetModal.title" ok-only @hide="resetresetModal">
          <form @submit.prevent="handleUpload">
            <div class="aat-modal-container">
              <fieldset class="aat-form-section">
                <legend class="aat-sub-header">
                  Confirm Reset
                </legend>
                <div id="reset_col_option">
                  <b-form-checkbox
                    id="col_reset_checkbox"
                    name="col_reset_checkbox"
                    value=""
                  >
                    Reassign all applications from "<span v-if="collectionType === 'Cohort'">Cohort </span>{{ resetModal.itemName }}" to <em>unassigned</em>.
                  </b-form-checkbox>
                </div>
              </fieldset>
              <fieldset class="aat-form-section">
                <legend class="aat-sub-header">
                  Add Comment
                </legend>
                <label for="reassignment_comment">Enter comment for this assignment.</label>
                <textarea id="reassignment_comment" v-model="comment" class="aat-comment-field" />
              </fieldset>
              <p v-if="resetModal.protect === 'Yes'">
                <b>Note:</b> This is a protected cohort.
              </p>
            </div>
          </form>
        </b-modal>
      </div>
    </template>
  </div>
</template>

<script>
  const axios = require("axios");
  export default {
    name: "CollectionList",
    components: {
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
            key: 'name',
            label: "Cohort #",
            class: "aat-data-cell aat-data-nowrap",
            sortable: true
          },
          {
            key: 'Description',
            class: "aat-data-cell",
            sortable: true
          },
          {
            key: 'Residency',
            class: "aat-data-cell",
            sortable: true,
          },
          {
            key: 'protect',
            label: 'Protected',
            class: "aat-data-cell",
            sortable: true
          },
          {
            key: 'Admit_Status',
            class: "aat-data-cell aat-data-nowrap",
            sortable: true
          },
          {
            key: 'Assigned',
            class: "aat-data-cell",
            sortable: true,
          },
          { key: 'actions', label: '', class: "aat-actions-cell aat-data-cell aat-data-nowrap", }
        ],
        cohorts: [],
        majorFields: [
          {
            key: 'name',
            label: 'Major',
            class: "aat-data-cell",
            sortable: true
          },
          {
            key: 'Division',
            class: "aat-data-cell",
            sortable: true
          },
          {
            key: 'College',
            class: "aat-data-cell",
            sortable: true,
          },
          {
            key: 'DTX',
            class: "aat-data-cell",
            sortable: true
          },
          {
            key: 'Assigned',
            class: "aat-data-cell",
            sortable: true
          },
          {
            key: 'Actions',
            label: '',
            class: "aat-actions-cell aat-data-cell aat-data-nowrap",
            sortable: false,
          }
        ],
        majors: [],
        resetModal: {
          id: 'reset-modal',
          title: ''
        },
        comment: '',
      };
    },
    mounted() {
      this.load_data();
    },
    methods: {
      load_data(){
        axios.get(
          '/api/collection/' + this.collectionType.toLowerCase() + "/",
        ).then(response => {
          if(this.collectionType.toLowerCase() === "cohort"){
            this.cohorts = response.data;
          } else if (this.collectionType.toLowerCase() === "major"){
            this.majors = response.data;
          }
        });
      },
      info(item, index, button) {
        this.resetModal.title = `Reset ${this.collectionType}`;
        this.resetModal.itemName = `${item.name}`;
        this.resetModal.protect = `${item.protect}`;
        this.$root.$emit('bv::show::modal', this.resetModal.id, button);
      },
      resetresetModal() {
        this.resetModal.title = '';
        this.resetModal.content = '';
      },
    }
  };
</script>

<style lang="scss">

  .aat-actions-cell a,
  .aat-actions-cell button {
    margin: 0 0.25rem;
  }
</style>
