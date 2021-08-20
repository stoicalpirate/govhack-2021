<template>
  <div>
    <b-navbar variant="light">
      <b-navbar-nav v-for="route in footerRoutes" :key="route.name" class="mx-auto">
        <b-nav-item :href="route.name">{{ route.title }}</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      footerRoutes: [
        {
          name: 'about',
          title: 'About',
        },
        {
          name: process.env.VUE_APP_MAILTO,
          title: 'Contact',
        },
        {
          name: 'terms',
          title: 'Terms',
        },
        {
          name: 'privacy',
          title: 'Privacy',
        },
      ],
    }
  },
}
</script>