/* コード.gs */
const SS = SpreadsheetApp.getActiveSpreadsheet();

function doGet(e) {
  let page = e.parameter.page;
  if (!page) page = 'family_home';
  return HtmlService.createTemplateFromFile(page)
    .evaluate()
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setTitle('ココイル');
}

/* --- 1. ログイン関連 (シートを参照してチェック) --- */
function checkLogin(inputId, inputPass) {
  // A. スタッフかどうかチェック
  const staffSheet = SS.getSheetByName('Staff');
  // データが空の場合のエラー回避
  if (staffSheet.getLastRow() > 1) {
    const staffData = staffSheet.getRange(2, 1, staffSheet.getLastRow() - 1, 3).getValues();
    for (let i = 0; i < staffData.length; i++) {
      // ID(0) と PASS(2) が一致したら
      if (staffData[i][0] == inputId && staffData[i][2] == inputPass) {
        return { success: true, type: 'employee', name: staffData[i][1] };
      }
    }
  }

  // B. 入居者かどうかチェック
  const resSheet = SS.getSheetByName('Residents');
  if (resSheet.getLastRow() > 1) {
    // Room(0), Name(1), ..., Password(4)
    const resData = resSheet.getRange(2, 1, resSheet.getLastRow() - 1, 5).getValues();
    for (let i = 0; i < resData.length; i++) {
      // Room(0) をID代わりにする
      if (String(resData[i][0]) == inputId && String(resData[i][4]) == inputPass) {
        return { success: true, type: 'resident', index: i };
      }
    }
  }

  return { success: false };
}

/* --- 2. 入居者データ操作 --- */
function getResidentsData() {
  const sheet = SS.getSheetByName('Residents');
  if (sheet.getLastRow() <= 1) return [];
  const values = sheet.getRange(2, 1, sheet.getLastRow() - 1, 4).getValues();
  return values.map(row => ({
    room: row[0],
    name: row[1],
    status: row[2],
    time: row[3]
  }));
}

// パスワード引数を追加
function addResident(room, name, password) {
  const sheet = SS.getSheetByName('Residents');
  const now = new Date();
  const timeStr = `${now.getHours()}:${String(now.getMinutes()).padStart(2,'0')} 登録`;
  // E列にパスワードを保存
  sheet.appendRow([room, name, '在室', timeStr, password]);
}

function deleteResident(index) {
  const sheet = SS.getSheetByName('Residents');
  sheet.deleteRow(index + 2);
}

/* --- 3. スタッフデータ操作 (新規追加) --- */
function getStaffData() {
  const sheet = SS.getSheetByName('Staff');
  if (sheet.getLastRow() <= 1) return [];
  const values = sheet.getRange(2, 1, sheet.getLastRow() - 1, 2).getValues();
  // パスワードは画面に返さない（セキュリティのため）
  return values.map(row => ({
    id: row[0],
    name: row[1]
  }));
}

function addStaff(id, name, password) {
  const sheet = SS.getSheetByName('Staff');
  sheet.appendRow([id, name, password]);
}

function deleteStaff(index) {
  const sheet = SS.getSheetByName('Staff');
  sheet.deleteRow(index + 2);
}

/* --- 4. ニュース・業務連絡 (変更なし) --- */
function getNewsData() {
  const sheet = SS.getSheetByName('News');
  if (sheet.getLastRow() <= 1) return [];
  const values = sheet.getDataRange().getValues();
  values.shift();
  return values.map(row => ({ date: row[0], title: row[1] }));
}
function addNews(title) {
  const sheet = SS.getSheetByName('News');
  const now = new Date();
  const dateStr = `${now.getMonth() + 1}/${now.getDate()}`;
  sheet.appendRow([dateStr, title]);
}
function deleteNews(index) {
  const sheet = SS.getSheetByName('News');
  sheet.deleteRow(index + 2);
}
function getMessagesData() {
  const sheet = SS.getSheetByName('Messages');
  if (sheet.getLastRow() <= 1) return [];
  const values = sheet.getDataRange().getValues();
  values.shift();
  return values.map(row => ({ date: row[0], title: row[1], content: row[2], author: row[3] }));
}
function addMessage(title, content, author) {
  const sheet = SS.getSheetByName('Messages');
  const now = new Date();
  const dateStr = `${now.getMonth() + 1}/${now.getDate()} ${now.getHours()}:${String(now.getMinutes()).padStart(2,'0')}`;
  sheet.appendRow([dateStr, title, content, author]);
}
function deleteMessage(index) {
  const sheet = SS.getSheetByName('Messages');
  sheet.deleteRow(index + 2);
}
