import Vue from 'vue';
import Router from 'vue-router';
// import DraftInit from '@/components/DraftInit';
import DraftMain from '@/components/drafting/DraftMain';
// import HelloWorld from '@/components/HelloWorld';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'DraftMain',
      component: DraftMain,
    },
  ],
  mode: 'hash',
});
