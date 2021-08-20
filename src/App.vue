<template>
  <Loading v-if="$root.isLoading" />
  <div v-else>
    <router-view />
  </div>  
</template>

<script>
import Loading from '@/components/Loading'

export default {
  name: "App",
  components: { Loading }
}
</script>

