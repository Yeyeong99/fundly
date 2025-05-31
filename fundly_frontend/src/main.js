import {createApp} from "vue";
import {createPinia} from "pinia";
import {definePreset} from "@primeuix/themes";
import Lara from "@primeuix/themes/lara";

import PrimeVue from "primevue/config";
import App from "./App.vue";
import router from "./router";
import ConfirmationService from "primevue/confirmationservice";
import "primeicons/primeicons.css";

const MyPreset = definePreset(Lara, {
  semantic: {
    primary: {
      50: "{slate.50}",
      100: "{slate.100}",
      200: "{slate.200}",
      300: "{slate.300}",
      400: "{slate.400}",
      500: "{slate.500}",
      600: "{slate.600}",
      700: "{slate.700}",
      800: "{slate.800}",
      900: "{slate.900}",
      950: "{slate.950}"
    }
  },
  components: {
    button: {
      root: {
        primary: {
          background: "{slate.900}",
          color: "white",
          border: "{slate.900}"
        },
        label: {
          fontWeight: 500
        }
      },
      text: {
        primary: {
          color: "{slate.900}"
        }
      },
      outlined: {
        primary: {
          color: "{slate.900}",
          border: "{slate.500}"
        }
      }
    }
  }
});

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(ConfirmationService);
app.use(PrimeVue, {
  theme: {
    preset: MyPreset
  }
});

app.mount("#app");
