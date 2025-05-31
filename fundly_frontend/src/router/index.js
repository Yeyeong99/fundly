import CheckGoal from "@/views/Goal/CheckGoal.vue";
import CheckProducts from "@/views/Product/CheckProducts.vue";
import CheckUser from "@/views/MyPage/CheckUser.vue";
import CheckSpot from "@/views/CheckSpot.vue";
import Community from "@/views/Community/Community.vue";
import CommunityDetail from "@/views/Community/CommunityDetail.vue";
import EditPassword from "@/views/MyPage/EditPassword.vue";
import EditPersonalInfo from "@/views/MyPage/EditPersonalInfo.vue";
import GoalDetail from "@/views/Goal/GoalDetail.vue";
import GoalProductDetail from "@/views/Goal/GoalProductDetail.vue";
import LikeProducts from "@/views/MyPage/LikeProducts.vue";
import Login from "@/views/Login/Login.vue";
import LoginSuccess from "@/views/Login/LoginSuccess.vue";
import ProductDetail from "@/views/Product/ProductDetail.vue";
import QnA from "@/views/MyPage/QnA.vue";
import RecommendProducts from "@/views/Product/RecommendProducts.vue";
import RecommendedResult from "@/views/Product/RecommendedResult.vue";
import SearchBank from "@/views/SearchBank.vue";
import SetGoal from "@/views/Goal/SetGoal.vue";
import Signup from "@/views/Signup/Signup.vue";
import {createRouter, createWebHistory} from "vue-router";
import WritePost from "@/views/Community/WritePost.vue";
import AddData from "@/views/Goal/AddData.vue";
import ShowYoutube from "@/views/ShowYoutube.vue";
import ChatBot from "@/views/ChatBot.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "checkgoal",
      component: CheckGoal
    }, {
      path: "/checkgoal/:goalid",
      name: "goaldetail",
      component: GoalDetail
    }, {
      path: "/checkgoal/edit/:goalid",
      name: "editgoal",
      component: SetGoal
    }, {
      path: "/checkgoal/:goalid/:userid/:product",
      name: "goalproductdetail",
      component: GoalProductDetail
    }, {
      path: "/checkgoal/:goalid/adddata",
      name: "goaladddata",
      component: AddData
    }, {
      path: "/checkproducts",
      name: "checkproducts",
      component: CheckProducts
    }, {
      path: "/checkproducts/:comeFrom/:id",
      name: "productdetail",
      component: ProductDetail
    },{
      path: "/checkproducts/connected/:comeFrom/goal/:goalid/product/:id",
      name: "connectedproductdetail",
      component: ProductDetail
    }, {
      path: "/community",
      name: "community",
      component: Community
    }, {
      path: "/writepost",
      name: "writepost",
      component: WritePost
    }, {
      path: "/community/edit/:id",
      name: "editpost",
      component: WritePost
    }, {
      path: "/community/detail/:id",
      name: "detail",
      component: CommunityDetail
    }, {
      path: "/edit/personalinfo",
      name: "editpersonalInfo",
      component: EditPersonalInfo
    }, {
      path: "/likeproducts",
      name: "likeproducts",
      component: LikeProducts
    }, {
      path: "/login",
      name: "login",
      component: Login
    }, {
      path: "/login/success",
      name: "loginsuccess",
      component: LoginSuccess
    }, {
      path: "/qna",
      name: "qna",
      component: QnA
    }, {
      path: "/recommendproducts",
      name: "recommendproducts",
      component: RecommendProducts
    }, {
      path: "/searchbank",
      name: "searchbank",
      component: SearchBank
    }, {
      path: "/setgoal",
      name: "setgoal",
      component: SetGoal
    }, {
      path: "/signup",
      name: "signup",
      component: Signup
    }, {
      path: "/edit/password",
      name: 'editpassword',
      component: EditPassword
    }, {
      path: "/checkuser",
      name: "checkuser",
      component: CheckUser
    }, {
      path: "/checkspot",
      name: "checkspot",
      component: CheckSpot
    }, {
      path: "/recommendedresult",
      name: "recommendedresult",
      component: RecommendedResult
    }, {
      path: '/showyoutube/:id',
      name: 'showyoutube',
      component: ShowYoutube
    }, {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatBot
    },
    
  ]
});

// 로그인 안되었으면 로그인 화면만 들어갈 수 있도록
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem("access_token");
  const publicPages = ["/login", "/signup", "/login/success"];

  if (!isLoggedIn && !publicPages.includes(to.path)) {
    next("/login");
  } else {
    next();
  }
});

export default router;
