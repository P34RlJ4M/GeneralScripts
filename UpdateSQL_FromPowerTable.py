## IS Cell Editable must be enabled and true

def onCellEdited(self, rowIndex, colIndex, oldValue, newValue):
	try:
		schedule_id = self.data.getValueAt(rowIndex, self.data.getColumnIndex("schedule_id"))
		end_time = newValue

		print "Updating schedule_id: {}, end_time: {}".format(schedule_id, end_time)

		if end_time is None:
			print "End time is None. Update skipped."
			system.gui.errorBox("End time is None. Update skipped.")
			return

		# Call named query (Vision Client Scope version)
		system.db.runNamedQuery("UpdateEndTime", {
			"schedule_id": schedule_id,
			"end_time": end_time
		})

		print "Update successful."

	except Exception as e:
		print "Error during update: {}".format(e)
		system.gui.errorBox("Update failed: {}".format(e))