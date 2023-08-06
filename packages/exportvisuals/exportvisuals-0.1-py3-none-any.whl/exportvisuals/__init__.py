import pandas as pd
import json
import openpyxl
import os
import pdfkit
import imgkit
import loggerutility as logger


class ExportVisual:
    val = ""
    column = ""
    final_df = None
    html_str = ""

    def export(self):
        userId = ""
        editorId = ""
        visualId = "new_visual"
        transpose = ""
        outputType = ""
        group = ""
        row = ""
        pivot_flag = False
        df = None
        exportType = ""
        group_style = ""

        # domData = request.get_data('jsonData', None)
        # domData = domData[9:]
        # jsonData = json.loads(domData)

        if 'visualId' in jsonData.keys():
            if jsonData.get('visualId') != None:
                visualId = jsonData['visualId']

        if 'editorId' in jsonData.keys():
            if jsonData.get('editorId') != None:
                editorId = jsonData['editorId']

        if 'userId' in jsonData.keys():
            if jsonData.get('userId') != None:
                userId = jsonData['userId']

        if 'exportType' in jsonData.keys():
            if jsonData.get('exportType') != None:
                exportType = jsonData['exportType']

        if 'visualJson' in jsonData.keys():
            if jsonData.get('visualJson') != None:
                visualJson = jsonData['visualJson']

        if 'columnHeading' in jsonData.keys():
            if jsonData.get('columnHeading') != None:
                columnHeading = jsonData['columnHeading']

        if 'oldColumnHeading' in jsonData.keys():
            if jsonData.get('oldColumnHeading') != None:
                oldColumnHeading = jsonData['oldColumnHeading']

        logger.log(f"\n exportType:  {exportType}", "0")
        df = self.read(userId, editorId, visualId, "final")

        visualJson1 = json.loads(visualJson)
        columnHeading = columnHeading.split(",")
        df.rename(columns=dict(zip(df.columns, columnHeading)), inplace=True)
        oldColumnHeading = oldColumnHeading.split(",")

        if 'groups' in visualJson1.keys():
            if len(visualJson1.get('groups')) != 0:
                group = visualJson1['groups']

        if 'rows' in visualJson1.keys():
            if len(visualJson1.get('rows')) != 0:
                row = visualJson1["rows"]

        if 'columns' in visualJson1.keys():
            if len(visualJson1.get('columns')) != 0:
                self.column = visualJson1["columns"]

        if 'values' in visualJson1.keys():
            if len(visualJson1.get('values')) != 0:
                self.val = visualJson1["values"]

        if len(group) != 0:
            lst = []
            for label, df_obj in (df).groupby(group):
                sum = df_obj[self.val].sum()
                df_obj.loc[' '] = sum
                lst.append(df_obj)
            self.final_df = pd.concat(lst)
            self.final_df.loc[self.final_df[row[0]].isnull(), group[0]] = "Total "
            self.final_df.loc[''] = df[self.val].sum()
            self.final_df.fillna('', inplace=True)
            self.final_df.iloc[-1, self.final_df.columns.get_loc(group[0])] = 'Grand Total '
            group_style = True
            self.html_str = self.getTableHTML(self.final_df, jsonData, group_style)

        elif len(self.column) == 0:
            self.html_str = self.getTableHTML(df, jsonData, group_style)

        else:
            pivot_flag = True
            self.final_df = pd.pivot_table(df, index=row, columns=self.column, values=self.val)
            self.html_str = self.getTableHTML(self.final_df, jsonData, group_style)

        if exportType == "HTML":
            self.exportToHtml(visualId, self.html_str)

        elif exportType == "IMAGE":
            self.exportToImage(visualId, self.html_str)

        elif exportType == "EXCEL":
            self.exportToExcel(visualId, self.final_df, pivot_flag)

        elif exportType == "PDF":
            self.exportToPdf(visualId, self.html_str, pivot_flag)

        elif exportType == "JSON":
            self.exportToJson(visualId, self.final_df)

    def read(self, userId, editorId, visualId, df_type):
        dir = '/Pickle_files'
        path = os.getcwd()
        logger.log(f"\n Current working directory:  {path}", "0")

        if os.path.exists(dir):
            filename = str(userId) + '_' + str(editorId) + '_' + str(visualId) + '_' + df_type
            if os.path.isfile(dir + '/' + filename + '.pkl'):
                pickle_obj = pd.read_pickle(dir + '/' + filename + '.pkl')
                return pickle_obj

    def format_num(self, str):
        return "text-align:right !important"

    def getTableHTML(self, df, jsonData, group_style):
        if group_style:
            pivot_style = (df).reset_index(drop=True).style.applymap(self.format_num, subset=self.val).format('{:.3f}',
                                                                                                              na_rep='',
                                                                                                              subset=self.val)

        else:
            pivot_style = (df).style.applymap(self.format_num, subset=self.val).format('{:.3f}', na_rep='',
                                                                                       subset=self.val)

        pivot_style = (pivot_style).set_table_attributes('class= "insight_html_table"')
        col_dtype = dict(zip((jsonData['columnHeading']).split(','), json.loads(jsonData['columndataTypes']).values()))

        if 'advancedFormatting' in jsonData.keys():
            if jsonData.get('advancedFormatting') != None:
                advancedFormatting = jsonData['advancedFormatting']

        if advancedFormatting:
            for i in advancedFormatting.keys():
                if col_dtype[i] == 'string':
                    pivot_style = pivot_style.set_properties(**{'background-color': advancedFormatting[i]}, subset=[i])
                else:
                    pivot_style = pivot_style.background_gradient(cmap=advancedFormatting[i], subset=[i])
        htmlStr = pivot_style.render()
        return htmlStr

    def exportToImage(self, visualId, html_str):
        filename = str(visualId)
        path_wkhtmltoimage = '/usr/local/bin/wkhtmltoimage'
        config = imgkit.config(wkhtmltoimage=path_wkhtmltoimage)
        imgkit.from_string(html_str, filename + '.png', config=config)
        logger.log(f"\n {filename}.png saved. ", "0")
        return filename + ".png"

    def exportToPdf(self, visualId, html_str, pivot_flag):
        filename = str(visualId)
        path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        option = {'page-height': '1000mm', 'page-width': '5000mm'}

        if pivot_flag:
            html_str = html_str.replace('NaN', '')
            pdfkit.from_string(html_str, filename + '.pdf', configuration=config, options=option)

        else:
            index = df.columns.get_loc(self.val[0])
            total = df[df.columns[index]].count()
            df.index = [i for i in range(0, (total.astype(int)))]
            html_str = html_str.replace('NaN', '')
            pdfkit.from_string(html_str, filename + '.pdf', configuration=config)
        logger.log(f"\n {filename}.pdf created. ", "0")
        return filename + ".pdf"

    def exportToExcel(self, visualId, df, pivot_flag):
        filename = str(visualId)
        if not pivot_flag:
            index = df.columns.get_loc(self.colum[0])
            total = df[df.columns[index]].count()
            df.index = [i for i in range(0, (total.astype(int)))]

        df.to_excel(filename + ".xlsx")
        logger.log(f"\n {filename}.xlsx created. ", "0")
        return filename + ".xlsx"

    def exportToJson(self, visualId, df):
        filename = str(visualId)
        jsonDf = df.to_json()
        with open(filename + ".json", "w") as f:
            f.write(jsonDf)
            logger.log(f"\n {filename}.json created. ", "0")
            return filename + ".json"

    def exportToHtml(self, visualId, htmlStr):
        filename = str(visualId)
        with open(filename + ".html", "w") as f:
            f.write(htmlStr)
            logger.log(f"\n {filename}.html created. ", "0")
            return filename + ".html"