function doGet(e) {
  return ContentService.createTextOutput("Google Script is running!");
}


function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Stock Data");
    const data = JSON.parse(e.postData.contents);
    const timestamp = new Date();

    // Write header if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Timestamp",
        "State",
        "SS Name",
        "DB Name",
        "Month",
        "Category",
        "Item",
        "Mrp",
        "Opening Stock",
        "Purchase",
        "Sales"
       
      ]);
    }

    // Loop through stocks entries
    data.stocks.forEach(item => {
      sheet.appendRow([
        timestamp,
        data.State,
        data.SS_Name,
        data.DB_Name,
        data.Month,
        item.Category,
        item.Item,
        item.Mrp,
        item.Opening,
        item.Purchase,
        item.Sales
        
      ]);
    });

    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
                         .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.message }))
                         .setMimeType(ContentService.MimeType.JSON);
  }
}
