<template>
  <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
      <li class="breadcrumb-item">
        <a :href="portalURL" @click.prevent.stop="fetchData(portalURL)"
          >Startpage</a
        >
      </li>
      <template v-for="(item, index) in breadcrumbs" :key="item['@id0']">
        <li class="breadcrumb-item" v-if="index != breadcrumbs.length - 1">
          <a :href="item['@id']" @click.stop.prevent="fetchData(item['@id'])">{{
            item.title
          }}</a>
        </li>
        <li v-else class="breadcrumb-item active" aria-current="page">
          {{ item.title }}
        </li>
      </template>
    </ol>
  </nav>
</template>
<script>
export default {
  props: {
    breadcrumbs: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    portalURL: {
      type: String,
      required: true,
      default: () => {
        return "";
      },
    },
    fetchData: {
      type: Function,
      required: true,
      default: () => {
        return null;
      },
    },
  },
};
</script>
