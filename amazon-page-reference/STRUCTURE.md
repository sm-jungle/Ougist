# Amazon 商品详情页 (DPP) 代码结构速查

参考页面: `https://www.amazon.com/dp/B0G4M937GT#immersive-view_1774959928401`

> 本文档总结 Amazon DPP 真实站点常见的 DOM ID / class 命名约定，配套
> `index.html` + `styles.css` 是一个可直接打开浏览的骨架仿真，
> 用作仿站 / 自己搭电商详情页时的对照表。

---

## 1. 整体骨架

```
<body>
 ├── <header id="navbar">                顶部双层导航 (nav-belt + nav-main)
 ├── <main id="dp" data-asin="...">      整个商品页根容器
 │    └── <div id="a-page">
 │         ├── #wayfinding-breadcrumbs_feature_div      面包屑
 │         ├── #centerCol_wrapper                       三列主体
 │         │    ├── #leftCol   → 图片区 #imageBlock
 │         │    ├── #centerCol → 标题 / 评分 / 价格 / Twister / Overview / About
 │         │    └── #rightCol  → Buy Box #desktop_buybox
 │         ├── #immersiveView_feature_div               沉浸式视图 (本页锚点)
 │         ├── #aplus_feature_div                       A+ 富文本
 │         ├── #productDetails_feature_div              规格表
 │         └── #reviewsMedley                           评论
 └── <footer id="navFooter">             页脚
```

### 命名约定

- Amazon 大量使用 `*_feature_div` 作为外层注入容器，便于服务端按 widget A/B 替换。
- 元素 ID 多用驼峰 `camelCase`，class 多用 Amazon UI 库 (AUI) 的 `a-` 前缀
  (`a-button`, `a-price`, `a-size-large`, `a-color-success` 等)。
- 价格区域同时含 `a-offscreen`(给屏幕阅读器) + `aria-hidden` 的视觉版本。

---

## 2. 三列主体细节

### 2.1 `#leftCol` — 图片画廊

| 容器 | 作用 |
| --- | --- |
| `#imageBlock_feature_div` | 服务端注入入口 |
| `#imageBlock` | 客户端 ImageBlock JS 实例化入口 |
| `#altImages` | 左侧缩略图列 |
| `#main-image-container` / `#ivLargeImage` | 主图容器 |
| `#landingImage` | 主图 `<img>`，`data-old-hires` 存放大图 URL |

### 2.2 `#centerCol` — 核心信息

| 容器 | 作用 |
| --- | --- |
| `#title_feature_div` → `#productTitle` | H1 标题 |
| `#bylineInfo` | 品牌 / Brand Store 链接 |
| `#averageCustomerReviews_feature_div` | 星级 + 评分数链接 |
| `#corePriceDisplay_desktop_feature_div` / `#apex_desktop` | 价格、折扣、配送提示 |
| `#twister_feature_div` → `#variation_color_name` / `#variation_size_name` | SKU 切换 |
| `#productOverview_feature_div` | 关键属性表 (品牌/材质/尺寸) |
| `#feature-bullets` | "About this item" 5 条卖点 |

### 2.3 `#rightCol` — Buy Box

| 容器 | 作用 |
| --- | --- |
| `#desktop_buybox_feature_div` / `#desktop_buybox` | 整个购买框 |
| `#corePrice_desktop` | 框内价格副本 |
| `#deliveryBlockMessage` / `#contextualIngressPtLabel_deliveryShortAddressV2` | 配送时间 + 地址 |
| `#availability` | 库存状态 (`In Stock` / `Only N left`) |
| `#qtySelectorContainer` | 数量选择 |
| `#submit.add-to-cart` / `#submit.buy-now` | 加购 / 立即购买 |
| `#addToWishList_feature_div` | 加心愿单 |

---

## 3. 沉浸式视图 (Immersive View)

URL 锚点 `#immersive-view_1774959928401` 直接对应一个 panel 节点：

```html
<section id="immersiveView_feature_div">
  <div id="immersive-view_<id>"
       class="immersive-view-panel"
       data-immersive-view-id="<id>">
    <div class="iv-panel-media"><img …></div>
    <div class="iv-panel-copy"><h2>…</h2><p>…</p></div>
  </div>
  …更多 panel 垂直堆叠
</section>
```

- 每个 panel 是一个全屏 (或大屏) 的图文卡片，左右布局，奇偶交替反转 (`iv-reverse`)。
- 锚点跳转可以直接定位到具体 panel，方便从外部链接到某个图文区段。

---

## 4. A+ 内容 (`#aplus_feature_div`)

- 根容器 `#aplus.aplus-v2.desktop.celwidget`，里面是 `aplus-module module-N` 的卡片。
- 常见模块：
  - `apm-brand-story` 品牌大图 + 标语
  - `apm-comparison-table` 对比表
  - `apm-image-row` 3 图横排
  - `apm-text-block` 富文本
- 品牌方上传，模板化，每个模块用 `apm-*` 前缀。

---

## 5. 规格表 / 评论 / 页脚

- `#productDetails_techSpec_section_1` 技术规格表，`th/td` 两列。
- `#reviewsMedley`：
  - `#cm_cr_dp_d_rating_histogram` 星级分布柱状图
  - `#cm-cr-dp-review-list` 评论列表，每条 `[data-hook="review"]`
- 页脚 `#navFooter` 三段：`#navBackToTop` 回到顶部条 + 四列链接 + 版权。

---

## 6. 关键 CSS 类速查 (AUI)

| 类 | 含义 |
| --- | --- |
| `a-size-{mini\|small\|base\|medium\|large}` | 字号梯度 |
| `a-color-{base\|success\|price\|secondary}` | 文本色梯度 |
| `a-spacing-{none\|micro\|mini\|small\|base\|medium\|large}` | 垂直外距 |
| `a-button` / `a-button-primary` / `a-button-base` | AUI 按钮 |
| `a-price` + `a-offscreen` | 价格组件 (含无障碍价) |
| `a-icon-star` + `a-star-{1..5}` / `a-star-4-5` | 星级图标 |
| `a-unordered-list a-vertical/a-horizontal a-nostyle` | 列表样式 |
| `a-declarative` | 绑定客户端事件的声明式标记 |
| `celwidget` | Amazon 客户体验 widget 容器 |

---

## 7. 如何用这份参考

1. 在浏览器里直接打开 `amazon-page-reference/index.html` 看骨架效果。
2. 想做自己产品页时，把 `#centerCol` / `#rightCol` / `#aplus` 等模块按需替换内容。
3. 关键 ID 保留，便于后续：
   - 写爬虫 / 解析器时按 Amazon 真实选择器命中。
   - 接入 widget A/B (基于 `*_feature_div` 容器替换)。
4. immersive-view 想接锚点跳转时，沿用 `#immersive-view_<id>` 命名，方便外链直达。

