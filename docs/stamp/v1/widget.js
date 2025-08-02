(function () {
  'use strict';

  const API_VERSION = 1;
  const LOCALHOST_PATTERN = /^(http:\/\/localhost:\d+)\//;
  const DEBUG_MODE = LOCALHOST_PATTERN.test(window.location.href);
  const API_URL_BASE = DEBUG_MODE ?
    `${window.location.href.match(LOCALHOST_PATTERN)[1]}/stamp/v${API_VERSION}` :
    `https://www.shapoco.net/stamp/v${API_VERSION}`;
  const URL_POSTFIX = '20250426145500';
  const COOKIE_KEY = 'ShapocoNetStamp_clientId';

  const CLASS_STAMP_BUTTON = 'shpcstamp_stamp';

  /** @type {ShapocoNetStamp|null} */
  let shapocoNetStamp = null;

  /** @type {Array} */
  let emojiCategories = [];

  /** @type {Object} */
  let emojiDict = {};

  /** @type {boolean} */
  let emojiDictLoaded = false;

  let commentRule = {
    maxLength: 64,
    ngWords: ['http://', 'https://', 'ftp://'],
    narrowCharPattern: '^[\\x00-\\x7e]$',
  };

  let maxStampCount = 3;

  let cssLoaded = false;
  let jsonLoaded = false;

  let stamps = {};
  let comments = [];
  let history = [];

  /** @type {EmojiPicker|null} */
  let emojiPicker = null;

  let commentWindow = null;

  /** @type {HTMLDivElement|null} */
  let stampContainer = null;

  /** @type {string|null} */
  let clientId = null;

  /** @type {string} */
  let pageLocation = window.location.href;

  const statusMsg = document.createElement('span');

  class ShapocoNetStamp {
    constructor() {
      this.stampButtonList = document.createElement('span');
      this.addButton = document.createElement('button');
      this.expandButton = document.createElement('button');

      stampContainer.classList.add('shpcstamp');

      this.stampButtonList.id = 'shpcstamp_stamp_list';
      this.stampButtonList.innerHTML = 'スタンプを読み込んでいます...&nbsp;';
      stampContainer.appendChild(this.stampButtonList);

      this.expandButton.type = 'button';
      this.expandButton.id = 'shpcstamp_expand_button';
      this.expandButton.title = '全てのスタンプを表示';
      this.expandButton.innerHTML = '全て表示';
      this.expandButton.style.display = 'none';
      stampContainer.appendChild(this.expandButton);
      this.expandButton.addEventListener('click', evt => this.onExpand(evt));

      this.addButton.type = 'button';
      this.addButton.id = 'shpcstamp_add_button';
      this.addButton.title = 'スタンプを追加する';
      this.addButton.innerHTML = '<span class="shpcstamp_emoji">➕</span>追加';
      stampContainer.appendChild(this.addButton);
      this.addButton.addEventListener('click', async (evt) => {
        if (commentWindow && commentWindow.isShown()) {
          commentWindow.hide();
        }
        if (emojiPicker && emojiPicker.isShown()) {
          emojiPicker.hide();
        }
        else {
          if (!emojiPicker) {
            emojiPicker = new EmojiPicker();
          }
          await emojiPicker.show(this.addButton);
        }
      });
    }

    /** 
     * @param {boolean} isFirstTime  
     */
    updateButtonList(isFirstTime) {
      // 自分が送ったスタンプの数
      const full = Object.values(stamps).filter(item => item.sent).length >= maxStampCount;

      // 既にあるボタンを更新する
      let tmpStamps = { ...stamps };
      const buttons = this.stampButtonList.querySelectorAll(`.${CLASS_STAMP_BUTTON}`);
      buttons.forEach(button => {
        const emoji = button.dataset.emoji;
        let numStamp = 0;
        let sent = false;
        if (emoji in tmpStamps) {
          numStamp = tmpStamps[emoji].count;
          sent = tmpStamps[emoji].sent;
          delete tmpStamps[emoji];
        }
        const numComment = comments.filter(comment => comment.emoji == emoji).length;
        this.updateButton(button, numStamp, numComment, sent, full);
      });

      // 足りないボタンを追加する
      let stampKeys = Object.keys(tmpStamps);
      if (isFirstTime) {
        // 初回はスタンプの数が多い順にソート
        stampKeys.sort((a, b) => {
          if (tmpStamps[a].count < tmpStamps[b].count) return 1;
          if (tmpStamps[a].count > tmpStamps[b].count) return -1;
          return 0;
        });
      }
      stampKeys.forEach(emoji => {
        const stamp = tmpStamps[emoji];
        const button = document.createElement('button');
        button.type = 'button';
        button.classList.add(CLASS_STAMP_BUTTON);
        button.addEventListener('click', async (evt) => await this.onStampClicked(button));
        button.addEventListener('wheel', evt => this.onStampWheel(button, evt));
        button.dataset.emoji = emoji;
        button.innerHTML =
          `<span class="shpcstamp_emoji">${replaceCustomEmoji(emoji)}</span>` +
          `<span class="shpcstamp_num_comment" style="background: url(${API_URL_BASE}/images/with_comment.svg);"></span>` +
          `<span class="shpcstamp_num_stamp"></span>`;
        const numComment = comments.filter(comment => comment.emoji == emoji).length;
        this.updateButton(button, stamp.count, numComment, stamp.sent, full);
        this.stampButtonList.appendChild(button);
      });

      if (isFirstTime) {
        // 自分が送ったスタンプとそれ以外を合わせて最大10種類まで表示
        const MAX_STAMPS_SHOWN = 10;

        // スタンプを何個まで表示するか決める
        let numShown = 0;
        this.stampButtonList.childNodes.forEach(button => {
          if (button.classList.contains('shpcstamp_sent')) {
            // 自分が送ったスタンプは常に表示
            numShown += 1;
            button.style.display = 'inline-block';
          }
        });

        this.stampButtonList.childNodes.forEach(button => {
          if (!button.classList.contains('shpcstamp_sent')) {
            // 自分が送ったスタンプは常に表示
            button.style.display = numShown < MAX_STAMPS_SHOWN ? 'inline-block' : 'none';
            numShown += 1;
          }
        });

        if (numShown > MAX_STAMPS_SHOWN) {
          // スタンプが10種類を超えた場合は「・・・」ボタンを表示する
          this.expandButton.style.display = 'inline-block';
        }
      }

      this.addButton.disabled = full;
      this.addButton.title = full ? `スタンプは ${maxStampCount} 個まで送れます` : 'スタンプを追加する';
    }

    updateButton(button, numStamp, numComment, sent, full) {
      const spanNumStamp = button.querySelector('.shpcstamp_num_stamp');
      spanNumStamp.innerHTML = numStamp;

      const spanNumComment = button.querySelector('.shpcstamp_num_comment');
      spanNumComment.style.display = numComment > 0 ? 'inline-block' : 'none';

      if (sent) {
        button.classList.add('shpcstamp_sent');
        button.title = 'スタンプを解除する';
      }
      else {
        button.classList.remove('shpcstamp_sent');
        button.title = full ? `スタンプは ${maxStampCount} 個まで送れます` : 'スタンプを送る';
      }
    }

    async onStampClicked(button) {
      if (emojiPicker && emojiPicker.isShown()) {
        emojiPicker.hide();
      }
      if (commentWindow && commentWindow.isShown() && commentWindow.ownerButton == button) {
        commentWindow.hide();
      }
      else {
        if (!commentWindow) {
          commentWindow = new StampViewer();
        }
        await commentWindow.show(button);
      }
    }

    onStampWheel(button, evt) {
      if (!(commentWindow && commentWindow.style.visibility == 'visible')) return;
      const wrapper = commentWindow.querySelector('.shpcstamp_comment_list');
      const ul = wrapper.querySelector('ul');
      if (ul.getBoundingClientRect().height <= wrapper.getBoundingClientRect().height) return;
      var amount = evt.deltaY;
      switch (evt.deltaMode) {
        case WheelEvent.DOM_DELTA_LINE: amount = evt.deltaY * 25; break;
        case WheelEvent.DOM_DELTA_PAGE: amount = evt.deltaY * 250; break;
      }
      wrapper.scrollBy({ top: amount, behavior: 'smooth' });
      evt.stopPropagation();
      evt.preventDefault();
    }

    onExpand(evt) {
      this.stampButtonList.childNodes.forEach(button => {
        button.style.display = 'inline-block';
      });
      this.expandButton.style.display = 'none';
    }

    async getPickerWindow() {
      if (!this.container) {
      }

      return this.container;
    }

    fixPopupPos(button, popup) {

    }

    /**
     * @param {boolean} enable 
     */
    setButtonEnables(enable) {
      const buttons = this.stampButtonList.querySelectorAll(`.${CLASS_STAMP_BUTTON}`);
      const cursor = enable ? 'pointer' : 'wait';
      buttons.forEach(button => {
        button.disabled = !enable;
        button.style.cursor = cursor;
      });
      this.addButton.disabled = !enable;
      this.addButton.style.cursor = cursor;
    }
  } // class ShapocoNetStamp

  class Popup {
    constructor(className) {
      /** @type {HTMLButtonElement|null} */
      this.ownerButton = null;

      this.container = document.createElement('form');
      this.container.classList.add('shpcstamp');
      this.container.classList.add('shpcstamp_popup');
      this.container.classList.add(className);
      this.container.style.visibility = 'hidden';
      this.container.style.zIndex = '999';
      this.container.onsubmit = 'return false;';
      document.body.appendChild(this.container);
    }

    async show(ownerButton) {
      this.ownerButton = ownerButton;

      // document.body に appendChild してもすぐには表示サイズを取得できないので
      // アニメーションを要求する
      window.requestAnimationFrame(t => {
        this.fixPos(this.addButton, this.container);
      });

      this.container.style.visibility = 'visible';
      this.fixPos();

      await this.onShow();
    }

    hide() {
      this.container.style.visibility = 'hidden';
    }

    isShown() {
      return this.container.style.visibility == 'visible';
    }

    fixPos() {
      if (!this.ownerButton) return;

      const buttonRect = this.ownerButton.getBoundingClientRect();
      const upperSpace = buttonRect.top;
      const lowerSpace = window.innerHeight - buttonRect.top + buttonRect.height;

      const pickerRect = this.container.getBoundingClientRect();
      let left = buttonRect.left + (buttonRect.width - pickerRect.width) / 2;
      if (left < 5) {
        left = 5;
      }
      else if (left + pickerRect.width > window.scrollX + window.innerWidth - 5) {
        left = window.scrollX + window.innerWidth - 5 - pickerRect.width;
      }

      var top = upperSpace > lowerSpace ?
        buttonRect.top + window.scrollY - pickerRect.height - 5 :
        buttonRect.bottom + window.scrollY + 5;

      this.container.style.position = 'position';
      this.container.style.left = left + 'px';
      this.container.style.top = top + 'px';
    }
  } // class Popup

  class StampViewer extends Popup {
    constructor() {
      super('shpcstamp_comment');

      this.commentTitleBar = document.createElement('h2');
      this.commentListDiv = document.createElement('div');
      this.commentBoxCtrl = new CommentBoxController();
      this.stampTitleBar = document.createElement('h2');
      this.stampDescDiv = document.createElement('p');
      this.sendButton = document.createElement('button');

      this.container.appendChild(this.commentTitleBar);
      this.commentListDiv.classList.add('shpcstamp_comment_list');
      this.container.appendChild(this.commentListDiv);
      this.stampTitleBar.textContent = 'スタンプの更新';
      this.container.appendChild(this.stampTitleBar);
      this.container.appendChild(this.stampDescDiv);
      this.container.appendChild(this.commentBoxCtrl.container);

      {
        const div = document.createElement('div');
        div.style.textAlign = 'right';
        const cancelButton = document.createElement('button');
        cancelButton.type = 'button';
        cancelButton.textContent = 'キャンセル';
        cancelButton.addEventListener('click', evt => this.hide());

        this.sendButton.type = 'button';
        this.sendButton.innerHTML = '<span class="shpcstamp_emoji">➕</span>スタンプを送信';

        div.appendChild(cancelButton);
        div.appendChild(document.createTextNode(' '));
        div.appendChild(this.sendButton);
        this.container.appendChild(div);
      }

      this.sendButton.addEventListener('click', async (evt) => this.onSend());
    }

    onShow() {
      const sent = this.checkSentThisStamp();

      const emoji = this.ownerButton.dataset.emoji;

      this.sendButton.innerHTML = sent ?
        `<span class="shpcstamp_emoji">${replaceCustomEmoji(emoji)}</span>スタンプを解除` :
        `<span class="shpcstamp_emoji">${replaceCustomEmoji(emoji)}</span>スタンプを送信`;
      this.commentBoxCtrl.clear();

      let numComments = 0;

      this.commentListDiv.innerHTML = '';
      const cts = comments.filter(entry => entry.emoji == emoji);
      this.commentTitleBar.innerHTML = `${cts.length} 件のコメント`;
      if (cts.length > 0) {
        const ul = document.createElement('ul');
        for (const entry of cts) {
          const li = document.createElement('li');
          li.innerHTML = escapeForHtml(entry.comment);
          ul.appendChild(li);
          numComments += 1;
        }
        this.commentListDiv.appendChild(ul);
        this.commentTitleBar.style.display = 'block';
        this.commentListDiv.style.display = 'block';
      }
      else {
        this.commentTitleBar.style.display = 'none';
        this.commentListDiv.style.display = 'none';
      }

      const numStampSent = Object.values(stamps).filter(item => item.sent).length;
      const full = numStampSent >= maxStampCount;
      if (sent) {
        this.stampTitleBar.innerHTML = `スタンプの解除`;
        this.stampDescDiv.textContent = '解除するとコメントも削除されます。';
      }
      else {
        this.stampTitleBar.innerHTML = `スタンプの送信`;
        if (full) {
          this.stampDescDiv.textContent = `スタンプは ${maxStampCount} 個までです。`;
        }
        else {
          this.stampDescDiv.textContent = getStampSendDescription();
        }
      }
      this.sendButton.disabled = !sent && full;
      this.commentBoxCtrl.setDisabled(!sent && full);

      this.commentBoxCtrl.container.style.display = sent ? 'none' : 'block';
    }

    checkSentThisStamp() {
      const emoji = this.ownerButton.dataset.emoji;
      return (emoji in stamps) ? (stamps[emoji].sent) : false;
    }

    async onSend() {
      const remove = this.checkSentThisStamp();
      const emoji = this.ownerButton.dataset.emoji;
      try {
        const comment = remove ? '' : this.commentBoxCtrl.getText();
        await updateStamp(emoji, remove, comment);
      }
      catch (error) {
        console.error(error);
        showMessage(false, '通信エラー');
      }
      this.hide();
    }

  } // class StampViewer

  class EmojiPicker extends Popup {
    constructor() {
      super('shpcstamp_picker');
      this.titleBar = document.createElement('h2');
      this.categoryList = document.createElement('select');
      this.emojiList = document.createElement('div');
      this.stampDescDiv = document.createElement('p');
      this.emojiBox = document.createElement('input');
      this.commentBoxCtrl = new CommentBoxController();
      this.sendButton = document.createElement('button');

      this.titleBar.textContent = 'スタンプの追加';
      this.container.appendChild(this.titleBar);

      // カテゴリ選択
      {
        this.categoryList.classList.add('shpcstamp_emoji');
        const div = document.createElement('div');
        div.appendChild(this.categoryList);
        this.container.appendChild(div);
      }

      // 絵文字のリスト
      {
        this.emojiList.textContent = '絵文字を読み込んでいます...';
        this.emojiList.classList.add('shpcstamp_popup_list');
        this.container.appendChild(this.emojiList);
      }

      // 説明文
      this.stampDescDiv.textContent = 'あと●個まで追加可能。';
      this.container.appendChild(this.stampDescDiv);

      // 絵文字の入力欄
      {
        this.emojiBox.type = 'text';
        this.emojiBox.classList.add('shpcstamp_emoji');
        this.emojiBox.style.width = '100%';
        this.emojiBox.placeholder = '↑から選択またはここに直接入力';
        const div = document.createElement('div');
        div.appendChild(this.emojiBox);
        this.container.appendChild(div);
      }

      // コメント欄
      this.container.appendChild(this.commentBoxCtrl.container);

      // ボタン
      {
        const cancelButton = document.createElement('button');
        cancelButton.type = 'button';
        cancelButton.textContent = 'キャンセル';

        this.sendButton.type = 'button';
        this.sendButton.innerHTML = '<span class="shpcstamp_emoji">➕</span>スタンプ送信';
        this.sendButton.disabled = true;

        const div = document.createElement('div');
        div.style.textAlign = 'right';
        div.appendChild(cancelButton);
        div.appendChild(document.createTextNode(' '));
        div.appendChild(this.sendButton);
        this.container.appendChild(div);

        cancelButton.addEventListener('click', evt => this.hide());
      }

      this.categoryList.addEventListener('change', evt => this.onStampCategoryChanged());
      this.emojiBox.addEventListener('change', evt => this.validate());
      this.emojiBox.addEventListener('keyup', async (evt) => await this.onPickerKeyUp(evt));
      this.sendButton.addEventListener('click', async (evt) => await this.send());
    }

    onStampCategoryChanged() {
      const icat = parseInt(this.categoryList.value);
      this.emojiList.innerHTML = '';
      var items = [];
      if (icat < 0) {
        items = history
          .filter(emoji => emoji in emojiDict)
          .map(emoji => emojiDict[emoji]);
      }
      else {
        items = emojiCategories[icat].items;
      }
      items.forEach(item => {
        const link = document.createElement('a');
        link.href = 'javascript:void(0)';
        link.classList.add('shpcstamp_emoji');
        link.title = item.name;
        link.dataset.emoji = item.emoji;
        link.innerHTML = replaceCustomEmoji(item.emoji);
        link.addEventListener('click', evt => this.onStampSelected(link));
        this.emojiList.appendChild(link);
      });

    }

    onStampSelected(link) {
      this.emojiBox.value = link.dataset.emoji;
      this.validate();
    }

    async onPickerKeyUp(evt) {
      const valid = this.validate();
      if (evt.keyCode == 13) { // Enter
        if (valid) await this.send();
      }
    }

    async onShow() {
      if (!emojiDictLoaded) {
        // emoji 辞書のロード
        emojiDictLoaded = true;
        try {
          const resp = await fetch(`${API_URL_BASE}/emoji.json?${URL_POSTFIX}`);
          const data = await resp.json();
          emojiCategories = data;
          for (const cate of data) {
            for (const item of cate.items) {
              emojiDict[item.emoji] = item;
            }
          }
        }
        catch (error) {
          console.error(error);
          this.emojiList.innerHTML = '通信エラー';
        }
      }
      
      this.stampDescDiv.textContent = getStampSendDescription();

      // カテゴリの選択肢を生成
      this.categoryList.innerHTML = '';
      const recentStamps = document.createElement('option');
      recentStamps.value = '-1';
      recentStamps.textContent = '⭐ 最近使われたスタンプ';
      this.categoryList.appendChild(recentStamps);
      for (let icat = 0; icat < emojiCategories.length; icat++) {
        const cate = emojiCategories[icat];
        const firstEmoji = cate.items[0].emoji;
        const option = document.createElement('option');
        option.value = icat.toString();
        if (firstEmoji.startsWith(':')) {
          option.textContent = cate.name;
        }
        else {
          option.textContent = `${firstEmoji} ${cate.name}`;
        }
        this.categoryList.appendChild(option);
        for (const item of cate.items) {
          if (item.emoji in emojiDict) {
            emojiDict[item.emoji].count += 1;
          }
        }
      }

      this.validate();
      this.onStampCategoryChanged();
      this.fixPos();
    }

    hide() {
      this.container.style.visibility = 'hidden';
    }

    validate() {
      const validEmoji = this.emojiBox.value in emojiDict;

      this.commentBoxCtrl.validate();
      const validComment = this.commentBoxCtrl.isValid;

      this.emojiBox.style.background = (!this.emojiBox.value || validEmoji) ? null : '#fcc';
      this.sendButton.disabled = !(validEmoji && validComment);
    }

    async send() {
      try {
        await updateStamp(this.emojiBox.value, false, this.commentBoxCtrl.getText());
        this.emojiBox.value = '';
        this.commentBoxCtrl.clear();
      }
      catch (error) {
        console.error(error);
        showMessage(false, '通信エラー');
      }
      this.hide();
    }

  } // class EmojiPicker

  class CommentBoxController {
    constructor() {
      this.container = document.createElement('div');
      this.textarea = document.createElement('textarea');
      this.lengthGuage = document.createElement('div');
      this.isValid = false;
      this.lengthPercent = 0;
      this.changeEvent = new Event('change');

      // コメント入力欄
      this.textarea = document.createElement('textarea');
      this.textarea.style.width = '100%';
      this.textarea.placeholder = '(コメントなし)';
      this.textarea.rows = 3;
      this.container.appendChild(this.textarea);

      // 文字数ゲージ
      const guageOuter = document.createElement('div');
      guageOuter.classList.add('shpcstamp_comment_len_outer');
      this.lengthGuage.classList.add('shpcstamp_comment_len_inner');
      this.lengthGuage.style.width = '0px';
      guageOuter.appendChild(this.lengthGuage);
      this.container.appendChild(guageOuter);

      this.textarea.addEventListener('change', evt => this.validate());
      this.textarea.addEventListener('keyup', async (evt) => {
        this.validate();
        this.container.dispatchEvent(this.changeEvent);
      });
    }

    validate() {
      this.isValid = true;
      const comment = this.getText();
      this.lengthPercent = 100 * calcCommentLength(comment) / commentRule.maxLength;
      if (this.lengthPercent > 100) {
        // コメントが長すぎる
        this.isValid = false;
      }
      else if (/<\/?\w+>/.test(comment)) {
        // HTMLタグのようなものを含む
        this.isValid = false;
      }
      else if (comment) {
        for (const ngWord of commentRule.ngWords) {
          if (comment.includes(ngWord)) {
            // NGワードを含む
            this.isValid = false;
            break;
          }
        }
      }

      // 文字数表示
      if (this.lengthPercent <= 100) {
        this.lengthGuage.style.width = Math.ceil(this.lengthPercent * 10) / 10 + '%';
        this.lengthGuage.style.background = null;
      }
      else {
        this.lengthGuage.style.width = '100%';
        this.lengthGuage.style.background = '#f00';
      }

      this.textarea.style.background = this.isValid ? null : '#fcc';

      return this.isValid;
    }

    getText() {
      return this.textarea.value.trim();
    }

    clear() {
      this.textarea.value = '';
      this.lengthGuage.style.width = '0px';
    }

    setDisabled(disabled) {
      this.textarea.disabled = disabled;
      this.textarea.style.background = disabled ? '#eee' : null;
    }

  } // class CommentBoxController

  /**
   * スタンプとコメントの追加・削除
   * @param {string} emoji 
   * @param {boolean} remove 
   * @param {string} comment 
   */
  async function updateStamp(emoji, remove, comment) {
    comment = comment.trim();
    var params = {
      s: pageLocation,
      m: remove ? 'd' : 'a',
      k: emoji,
    };
    if (clientId) params['i'] = clientId;
    if (comment) params['c'] = comment;

    const resp = await fetchApi(params);
    if (DEBUG_MODE) console.log(resp);
    procApiResponse(resp);
    if (resp.success) {
      shapocoNetStamp.updateButtonList(false);
    }
  }

  function procApiResponse(resp) {
    showMessage(resp.success, resp.message);
    if (resp.success) {
      stamps = resp.stamps;
      comments = resp.comments;
      history = resp.history;
      comments.reverse(); // 新着順にする
    }

    // クライアントIDの有効期限
    let clientIdMaxAge = 86400;
    if (resp.clientIdMaxAge) {
      clientIdMaxAge = Math.max(3600, Math.min(86400 * 365 * 3, Math.round(resp.clientIdMaxAge)));
    }
    else {
      console.warn('resp.clientIdMaxAge not found.');
    }

    // クライアントIDの保存
    if (resp.clientId) {
      clientId = resp.clientId;
      document.cookie =
        `${COOKIE_KEY}=${encodeURIComponent(clientId)}; ` +
        `Path=/; ` +
        `max-age=${clientIdMaxAge}; ` +
        `SameSite=Lax; ` +
        `Secure`;
    }
    else {
      console.warn('resp.clientId not found.');
    }

    // コメントのルール取得
    if (resp.commentRule) {
      commentRule = resp.commentRule;
    }
    else {
      console.warn('resp.commentRule not found.');
    }

    // スタンプの最大数
    if (resp.maxStampCount) {
      maxStampCount = Math.max(1, Math.min(10, resp.maxStampCount));
    }
    else {
      console.warn('resp.maxStampCount not found.');
    }
  }

  /**
   * @param {Object.<string, string>} params
   * @returns {Promise<Response>}
   */
  async function fetchApi(params) {
    setButtonEnables(false);
    const encodedParams = Object.keys(params)
      .map(key => `${key}=${encodeURIComponent(params[key])}`).join('&');
    const url = `${API_URL_BASE}/api.php?${encodedParams}`;
    if (DEBUG_MODE) console.log(url);
    const resp = await fetch(url);
    setButtonEnables(true);
    return resp.json();
  }

  /**
   * @param {boolean} enable 
   */
  function setButtonEnables(enable) {
    shapocoNetStamp.setButtonEnables(enable);
  }

  function getStampSendDescription() {
    const numStampSent = Object.values(stamps).filter(item => item.sent).length;
    return `あと ${maxStampCount - numStampSent} 個送信できます。コメントは任意で、他の人からも見えます。`;
  }

  /**
   * @param {string} s 
   * @returns {string}
   */
  function escapeForHtml(s) {
    return s
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;')
      .replaceAll(" ", '&nbsp;')
      .replaceAll("　", '&#x3000;');
  }

  /**
   * @param {string} s 
   * @returns {number}
   */
  function calcCommentLength(s) {
    const narrow = new RegExp(commentRule.narrowCharPattern);
    var len = 0;
    const n = s.length;
    for (var i = 0; i < n; i++) {
      len += narrow.test(s[i]) ? 1 : 2;
    }
    return len;
  }

  async function main() {
    if (DEBUG_MODE) {
      console.log('--------- DEBUG MODE --------');
      console.log(`API_URL_BASE = ${API_URL_BASE}`);
    }

    // クライアントIDの取得
    document.cookie.split(';').forEach(entry => {
      const kv = entry.trim().split('=');
      if (kv[0].trim() == COOKIE_KEY) {
        clientId = decodeURIComponent(kv[1].trim());
        if (DEBUG_MODE) {
          console.log(`clientId=${clientId}`);
        }
      }
    });

    // スタンプ表示場所の取得
    stampContainer = document.querySelector('#shpcstamp_wrap');
    if (!stampContainer) {
      console.warn('#shapoconet_stamp_wrap is deprecated.');
      stampContainer = document.querySelector('#shapoconet_stamp_wrap');
    }

    shapocoNetStamp = new ShapocoNetStamp();

    statusMsg.classList.add('shpcstamp_status');
    statusMsg.style.visibility = 'hidden';
    stampContainer.appendChild(statusMsg);

    // CSSのロード
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `${API_URL_BASE}/widget.css?${URL_POSTFIX}`;
    document.body.append(link);
    link.addEventListener('load', evt => {
      cssLoaded = true;
      if (DEBUG_MODE) console.log("CSS loaded.");
      onResourceLoaded();
    });

    let params = { s: pageLocation };
    if (clientId) params['i'] = clientId;
    try {
      const resp = await fetchApi(params);
      if (DEBUG_MODE) console.log(resp);
      procApiResponse(resp);
      jsonLoaded = true;
      if (DEBUG_MODE) console.log("JSON loaded.");
      onResourceLoaded();
    }
    catch (error) {
      console.error(error);
      shapocoNetStamp.stampButtonList.innerHTML = '';
      showMessage(false, 'スタンプを読み込めませんでした');
    }
  }

  function onResourceLoaded() {
    if (cssLoaded && jsonLoaded) {
      shapocoNetStamp.stampButtonList.innerHTML = '';
      shapocoNetStamp.updateButtonList(true);
    }
  }

  function showMessage(success, message) {
    if (success) {
      statusMsg.style.visibility = 'hidden';
      statusMsg.innerHTML = '';
    }
    else {
      statusMsg.innerHTML = '⚠ ' + (message ? message : '不明なエラー');
      statusMsg.style.visibility = 'visible';
    }
  }

  function replaceCustomEmoji(s) {
    const m = s.match(/^:(\w+):$/);
    if (m) {
      return `<img class="shpcstamp_custom_emoji" src="${getCustonEmojiUrl(m[1])}">`;
    }
    else {
      return s;
    }
  }

  function getCustonEmojiUrl(s) {
    const m = s.match(/^:(\w+):$/);
    if (m) s = m[1];
    return `${API_URL_BASE}/images/emoji64/${s}.png`;
  }

  // call main on page loaded
  window.addEventListener('load', async () => { await main(); });

})();
