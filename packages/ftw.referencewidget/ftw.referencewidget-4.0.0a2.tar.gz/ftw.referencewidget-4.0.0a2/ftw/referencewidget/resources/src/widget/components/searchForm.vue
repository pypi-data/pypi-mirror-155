<template>
  <form
    @submit.stop.prevent="search"
    class="row my-2 gy-2 gx-3 align-items-center"
  >
    <div class="col">
      <div class="form-floating">
        <select
          class="form-select"
          id="sortattr"
          aria-label="Sort attribute"
          v-model="sortOn"
          @change="() => search()"
        >
          <template
            v-for="(option, index) in sortAttribute"
            :key="option.value"
          >
            <option :selected="index == 0" :value="option.value">
              {{ option.title }}
            </option>
          </template>
        </select>
        <label for="sortattr">Sort on</label>
      </div>
    </div>
    <div class="col">
      <div class="form-floating">
        <select
          class="form-select"
          id="sortorder"
          aria-label="Sort order"
          v-model="sortOrder"
          @change="() => search()"
        >
          <option selected value="ascending">Ascending</option>
          <option selected value="descending">Descending</option>
        </select>
        <label for="sortorder">Sort order</label>
      </div>
    </div>
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          id="searchFilter"
          placeholder="Text"
          v-model="searchTerm"
        />
        <label for="searchFilter">Search</label>
      </div>
    </div>
    <div class="col">
      <button type="submit" class="btn btn-primary">Search</button>
      <button @click.stop.prevent="reset" class="btn btn-danger">
        Reset
      </button>
    </div>
  </form>
</template>
<script>
export default {
  data() {
    return {
      searchTerm: "",
      sortOn: "getObjPositionInParent",
      sortOrder: "ascending",
      sortAttribute: [
        { title: "Position", value: "getObjPositionInParent" },
        { title: "Title", value: "sortable_title" },
        { title: "Created", value: "created" },
        { title: "Modified", value: "modified" },
      ],
    };
  },
  methods: {
    search() {
      this.$emit("search", {
        searchTerm: this.searchTerm,
        sortOn: this.sortOn,
        sortOrder: this.sortOrder,
      });
    },
    reset() {
      this.$emit("reset", {
        searchTerm: "",
        sortOn: "getObjPositionInParent",
        sortOrder: "ascending",
      });
    },
  },
};
</script>
